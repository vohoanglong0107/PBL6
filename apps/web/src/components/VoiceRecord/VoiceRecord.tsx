import axios from "@/api/axios";
import * as React from "react";
import useRecorder from "./useRecorder";
import styles from "./VoiceRecord.module.scss";
import FormData from "form-data";
import { useRouter } from "next/router";



export default function VoiceRecord() {
 
  let { audioURL, audioBlob, isRecording, startRecording, stopRecording } = useRecorder();
  const refreshPage = () => {
      window.location.reload();
  };
  const router = useRouter();
  const predictSong = () => {
    var form = new FormData();
    const file = new File([audioBlob], "song")
    console.log(file)
    form.append("query", file);
    return axios.post('/predictions', form);
  };
  const handleUploadClick = (e: any) => {
    predictSong().then((results) =>
      router.push({
        pathname: "/showresult",
        query: { results: JSON.stringify({ data : results["data"]})}
      })
    )
  }

  return (
    <section className={styles.Section}>
      <div className={styles.Box}>
        <audio src={audioURL} controls className={styles.Audio} />
        <div className={styles.Btn}>
          <button
            onClick={startRecording}
            disabled={isRecording}
            className={styles.BtnRecord}
          >
            Start recording
          </button>
          <button
            onClick={stopRecording}
            disabled={!isRecording}
            className={styles.BtnStop}
          >
            Stop recording
          </button>
          <button onClick={refreshPage} className={styles.BtnReset}>
            Reset
          </button>
          <button onClick={handleUploadClick} className={styles.BtnSend}>
            Send
          </button>
        </div>
        <p className={styles.Paragraph}>
          <em className={styles.Text}>
            (Please allow us for using micro to record audio)
          </em>
        </p>
      </div>
    </section>
  );
}
