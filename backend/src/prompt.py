from langchain_core.prompts import ChatPromptTemplate


# question prompt
question_prompt = ChatPromptTemplate.from_template("""
You are an AI assistant that generates exactly 20 meaningful question–answer pairs from the given text.

Context:
{text}

Instructions:
- Read the text carefully.
- Generate exactly 20 unique and non-repetitive questions.
- Do not include numbering, introductory phrases, or filler lines. 
- Do not include answers in this step. 
Question:
""")
 
# this is the answer prompt
answer_prompt = ChatPromptTemplate.from_template("""
You are an AI assistant that provides accurate and concise answers to the given question on the context below.
Use only the information retrieved by the system to answer.
<context>
{context}
</context>                                                                                     
Question: {input}
Instructions:
- Provide a clear and concise answer to the question.
- Do not add extra commentary or explanations; only answer the question.
- If the answer is not in the context, respond with "N/A".
- The answer must be a single complete sentence or short paragraph, not a list, unless the question explicitly asks for a list.
Answer:
""")