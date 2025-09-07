# import tools
from dotenv import load_dotenv
load_dotenv()
import os
from pdf2image import convert_from_path
import glob
import json

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from src.prompt import question_prompt, answer_prompt
import  csv

# load openai api key
groq_api_key = os.getenv("GROQ_API_KEY")

# create openai embedding
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# load openai llm
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_api_key, temperature=0.8)


# file processing with embedding
def file_procession(file_path):

    # load pdf file
    loader = PyPDFLoader(file_path)
    docs = loader.load()    

    # split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)
    
    return documents

# this is llm pipeline
def llm_pipeline(file_path):
    documents = file_procession(file_path)

    # save vector store database
    vector_store = FAISS.from_documents(documents, embedding)

    parser = StrOutputParser()
    question_chain = question_prompt | llm | parser
    # refine_chain = refine_prompt | llm | parser

    all_questions = []
    number_of_question = 20
    for document in documents:
        # Generate initial questions
        initial_questions = question_chain.invoke({"text": document.page_content})
        
        # Parse the refined questions
        questions = [q.strip() for q in initial_questions.split("\n") if q.strip() != ""]
        
        for q in questions:
            if q not in all_questions:
                all_questions.append(q)

            if len(all_questions) >= number_of_question:
                break

        if len(all_questions) >= number_of_question:
                break
 
    # create answer chain
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    answer_chain = create_stuff_documents_chain(llm=llm, prompt=answer_prompt)
    rag_chain = create_retrieval_chain(retriever, answer_chain)

    # file uploaded base directory
    output_dir = "static/output"
    # if exists the any file then remove the file
    existing_files = glob.glob(os.path.join(output_dir, "*"))
    for f in existing_files:
        os.remove(f)

    csv_output_path = os.path.join(output_dir, "question_answer.csv")
    json_output_path = os.path.join(output_dir, "question_answer.json")

    results = []

    with open(csv_output_path, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Answer"])  # header row

        for question in all_questions:
            response = rag_chain.invoke({"input": question})
            # Write to CSV
            writer.writerow([question, response['answer']])

            # Store for JSON
            results.append({"Question": question, "Answer": response['answer']})


    # Save JSON file
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)