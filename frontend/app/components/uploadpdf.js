"use client"
import React, { use, useState } from "react";
import styles from './upload.module.css'
import Image from "next/image";
import FileImage from '@/public/file_upload.png'
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import Swal from 'sweetalert2' 


export default function UploadPDF({ children }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false)
    const [uploadFileName, setUploadFileName] = useState("")
    const [toggle, setToggle] = useState(false) 

    const handleFileChange = (e) => {
        const files = e.target.files[0]
        setFile(files);
        setUploadFileName(files.name)
    };

    // file uploaded function
    const handleUpload = async () => {
        if (!file) {
            alert("Please upload a PDF file");
            return;
        }
      
        const filename = file.name;
        const ext = filename.split(".").pop().toLowerCase();
        console.log(filename)

        if (ext === "pdf") {
            const formData = new FormData();
            formData.append("file", file);
            console.log(formData)

            try {
                setLoading(true)
                const res = await fetch("http://127.0.0.1:8000/upload", {
                    method: "POST",
                    body: formData,
                });

                if (!res.ok) throw new Error("Upload failed");
                const data = await res.json(); 
                console.log(data)
            } catch (error) {
                console.error("Upload failed", error);
            }
            finally {
                setLoading(false)
                setToggle(true)
                Swal.fire({
                  title: "Q&A Generated Successfully",
                  icon: "success",
                  draggable: true
              });
            }
        } else {
            alert("Only PDF files are allowed");
            setMessage("Invalid file type!");
        }
    };
    
    // Get csv file 
    const handleDownloadCSV = async () => {
        const response = await fetch("http://127.0.0.1:8000/csv-file")

        if(!response.ok) return

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
       
        const a = document.createElement("a");
        a.href = url;
        a.download = "question_answer.csv";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

    }
   
    // get json file
    const handleDownloadJSON = async () => {
        const response = await fetch("http://127.0.0.1:8000/json-file")

        if(!response.ok) return

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
       
        const a = document.createElement("a");
        a.href = url;
        a.download = "question_answer.json";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

    }

 
  return (
        <> 
          <div className={styles.upload_section_inner}> 
            <div className="text-center">
              <h2 className={styles.title}>AI-Powered Q&A Generator </h2>
              <p className={styles.subtitle}>Upload your data files and let AI generate intelligent questions and answers</p>
            </div>
            <div className={styles.upload_wrapper} onClick={() => document.getElementById('fileInput').click()}>
                <input 
                  className={styles.listing_file_up} 
                  type="file" 
                  onChange={handleFileChange}
                  id="fileInput"
                  />  
                <Image src={FileImage} alt="file_upload"  />
                <p>Clicl here or drop files to upload</p>     
                {uploadFileName && <p className={styles.upload_file_name}>Uploaded Fine: {uploadFileName}</p>}                          
            </div>  
            <button
              onClick={handleUpload}
              className={styles.action_btn}
              disabled={loading}
            >

            { loading ?  <div className="flex justify-center items-center"><AiOutlineLoading3Quarters className="animate-spin text-white text-4xl" /></div> : "🤖 Generate Q&A"}
             
            </button>
          </div>
          
          {toggle && <div className={styles.results_section}>
            <h2 className={styles.section_title}>✨ Q&A Generated Successfully!</h2> 
            <div className={styles.download_options}>
                <div className={`${styles.download_box} ${styles.csv_box}`}>
                    <div className={`${styles.download_icon} ${styles.csv_icon}`}>CSV</div>
                    <div className={styles.download_title}>CSV Format</div>
                    <div className={styles.download_desc}>Download as spreadsheet for analysis</div>
                    <button onClick={handleDownloadCSV} className={styles.download_btn}>📥 Download CSV</button>
                </div>
                
                <div className={`${styles.download_box} ${styles.json_box}`}>
                    <div className={`${styles.download_icon} ${styles.json_icon}`}>JSON</div>
                    <div className={styles.download_title}>JSON Format</div>
                    <div className={styles.download_desc}>Download as structured data format</div>
                    <button onClick={handleDownloadJSON} className={styles.download_btn}>📥 Download JSON</button>
                </div>
            </div> 
              { children }
          </div>}
          </>
    
  );
}
