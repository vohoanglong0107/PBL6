import Router, { useRouter } from "next/router";
import React, { useState } from "react";
import axios from "@/api/axios";
import styles from "./SongSearchForm.module.scss";
import FormData from "form-data";

export default function SongSearchForm() {
  const predictSong = async () => {
    var form = new FormData();
    form.append("query", file);
    return await axios
      .get("/predictions", { data: form })
      .then((res) => console.log(res));
  };

  const [file, setFile] = useState<File>();
  const router = useRouter();

  const handleFileChange = (e: any) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
      console.log("success");
      console.log(e.target.files);
    }
  };

  const handleUploadClick = (e: any) => {
    e.preventDefault();
    predictSong().then(() => router.push("/showresult"));
    // router.push("/showresult");
    // console.log("success");
  };
  return (
    <>
      <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
      ></meta>
      <br />

      <div className={styles.Contentleft}>
        <div className={styles.CoverTitle}>
          <p className={styles.Title}>Have you</p>
          <p className={styles.Title1}>
            ever had trouble listening <br /> to a piece of music but don
            {"'"}t know it{"'"}s name?
          </p>
          <p className={styles.Title2}>
            Don{"'"}t worry, Music RegZ will help you find it !
          </p>
          <form onSubmit={handleUploadClick}>
            <div className={styles.UploadFile}>
              <label className={styles.Label1} htmlFor="Label1">
                Click the side button to upload file
              </label>
              <input
                type={"file"}
                className={styles.Button1}
                onChange={handleFileChange}
                accept={".mp3, .mp4, wav"}
                required
              />
              <button className={styles.Button2}>Gửi</button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
function clsx(arg0: string): string | undefined {
  throw new Error("Function not implemented.");
}
