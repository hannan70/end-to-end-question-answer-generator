import getData from "../api/getData";
import styles from './upload.module.css'

export default async function Answer(){
    // get all question
    const res = await getData()
    const datas = res.data

    return (
        <>
            {datas?.map((data, index) => {
                return (
                    <div className={styles.qa_item} key={index}>
                        <div className={styles.question}>
                            <span className={styles.question_icon}>Q{index+1}</span>
                            {data.Question}
                        </div>
                        <div className={styles.answer}>
                            {data.Answer}
                        </div>
                    </div>
                )
            })}
              
        </>

    )
}