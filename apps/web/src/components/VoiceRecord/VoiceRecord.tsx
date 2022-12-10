import * as React from "react";
import { render } from "react-dom";
import useRecorder from "./useRecorder";
import styles from "./VoiceRecord.module.scss";

export default function VoiceRecord() {
  let { audioURL, isRecording, startRecording, stopRecording } = useRecorder();
  return (
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
        <button
          onClick={stopRecording}
          disabled={!isRecording}
          className={styles.BtnReset}
        >
          Reset
        </button>
        <button
          onClick={stopRecording}
          disabled={!isRecording}
          className={styles.BtnSend}
        >
          Send
        </button>
      </div>
      <p className={styles.Paragraph}>
        <em className={styles.Text}>
          (Please allow us for using micro to record audio)
        </em>
      </p>
    </div>
  );
}

// const rootElement = document.getElementById("root");
// render(<VoiceRecord/>, rootElement);
