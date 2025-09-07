import React from "react";
import styles from './upload.module.css' 
import UploadPDF from "./uploadpdf";
import Answer from "./anwser";
 
export default function Project() {
   
 
  return (
    <div className={styles.upload_section}>   

          <UploadPDF>
            <Answer />  
          </UploadPDF> 
          
    </div>
    
  );
}
