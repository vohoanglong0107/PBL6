import React from "react";
import classNames from "classnames";
import styles from "./ShowResult.module.scss";
import Image from "next/image";
import Logo from "@/assets/logo.svg";
import Avt from "@/assets/avt.jpg";
import Lover from "@/assets/lover.jpg";
import Head from "next/head";


export default function ShowResult() {
  return (
    <>
      
      <section className={styles.Section}>
        <div className={styles.Content}>
          <div className={styles.info_song}>
            <div className={styles.info}>
              <div className={styles.songs}>
                <h5 className={styles.song}>Song</h5>
                <p className={styles.song_name}>London Boy</p>
              </div>
              <div className={styles.artists}>
                <h5 className={styles.artist}>Artist</h5>
                <p className={styles.artist_name}>Taylor Swift</p>
              </div>
            </div>
            <div className={styles.image_Lover}>
              <Image
                src={Lover}
                alt="image description"
                height={215}
                width={231}
              />
            </div>
          </div>
          <div className={styles.UploadFile}>
            {/* <input className={styles.Input} /> */}
            <label className={styles.Label1} htmlFor="Label1">
              Click the right button to upload file
            </label>
            <input type={"file"} className={styles.Button1} />
          </div>


        </div>
        <div className={styles.image_avt}>
          <Image
            className="max-w-xs h-auto"
            src={Avt}
            alt="image description"
            height={500}
            width={400}
          />
        </div>
      </section>
    </>
  );
}
