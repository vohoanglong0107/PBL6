
import className from "classnames";
import styles from "./ShowResult.module.scss";
import Image from "next/image";
import Router, { useRouter } from "next/router";
import React, { useState } from "react";
import Lover from "@/assets/lover.jpg";
import Head from "next/head";
import Banner from "../Banner";

export default function ShowResult() {
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
    router.push("/showresult");
    console.log("success");
  };
  return (
    <>
      <section className={styles.Section}>
        <div className={styles.Content}>
          <div className={styles.info_song}>
            <div className={styles.info}>
              <div className={styles.songs}>
                <h5 className={styles.song}>Song</h5>
                <p className={styles.song_name}>London Boy</p>
                <p className={styles.sub_song_name1}>Good For You</p>
                <p className={styles.sub_song_name2}>
                  We Don{"'"}t Talk Anymore
                </p>
                <p className={styles.sub_song_name3}>Baby</p>
                <p className={styles.sub_song_name4}>Shape Of You</p>
              </div>
              <div className={styles.artists}>
                <h5 className={styles.artist}>Artist</h5>
                <p className={styles.artist_name}>Taylor Swift</p>
                <p className={styles.sub_artist_name1}>Selena Gomez</p>
                <p className={styles.sub_artist_name2}>Charlie Puth</p>
                <p className={styles.sub_artist_name3}>Justin Bieber</p>
                <p className={styles.sub_artist_name4}>Ed Sheeran</p>
              </div>
            </div>
          </div>
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
        <div className={styles.image_avt}>
          <Banner />
        </div>
      </section>
    </>
  );
}
