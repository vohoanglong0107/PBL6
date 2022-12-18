import { useEffect, useState } from "react";
import { MediaRecorder, register } from "extendable-media-recorder";
import { connect } from "extendable-media-recorder-wav-encoder";
import dynamic from "next/dynamic";

// const MediaRecorder = dynamic(
//   () => import("extendable-media-recorder").then((mod) => mod.MediaRecorder),
//   { ssr: false }
// );

const useRecorder = () => {
  const [audioURL, setAudioURL] = useState("");
  const [audioBlob, setAudioBlob] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [recorder, setRecorder] = useState(null);

  useEffect(() => {
    // Lazily obtain recorder first time we're recording.
    if (recorder === null) {
      if (isRecording) {
        requestRecorder().then(setRecorder, console.error);
      }
      return;
    }

    // Manage recorder state.
    if (isRecording) {
      recorder.start();
    } else {
      recorder.stop();
    }

    // Obtain the audio when ready.
    const handleData = (e) => {
      setAudioURL(URL.createObjectURL(e.data));
      setAudioBlob(e.data);
      console.log(e.data);
    };

    recorder.addEventListener("dataavailable", handleData);
    return () => recorder.removeEventListener("dataavailable", handleData);
  }, [recorder, isRecording]);

  const startRecording = () => {
    setIsRecording(true);
  };

  const stopRecording = () => {
    setIsRecording(false);
  };

  return {
    audioURL,
    audioBlob,
    isRecording,
    startRecording,
    stopRecording,
  };
};

async function requestRecorder() {
 await register(await connect());
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const options = { mimeType: "audio/wav" };
  
  const recorder = new MediaRecorder(stream, options);
  console.log(recorder.mimeType)
  return recorder
}
 
export default useRecorder;
