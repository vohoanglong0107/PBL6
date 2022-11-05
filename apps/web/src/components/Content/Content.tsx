import React from "react";
import styles from "./Content.module.scss";
import Image from "next/image";
import Logo2 from "@/assets/logo2.svg";
import Navbar from "../Navbar";
export default function Content() {
  return (
    <>
      {/* <Navbar /> */}
      <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
      ></meta>
      <br />
      <section className={styles.Section}>
        <div className={styles.Content}>
          <div className={styles.Contentleft}>
            <div className={styles.CoverTitle}>
              {/* <div className={styles.Text}> */}
                <p className={styles.Title}>Have you</p>
                <p className={styles.Title1}>
                  ever had trouble listening <br/> to a piece of music but don{"'"}t know it{"'"}s name?
                </p>
                <p className={styles.Title2}>
                  Don{"'"}t worry, Music RegZ will help you find it !
                </p>
              {/* </div> */}

              <div className={styles.UploadFile}>
                {/* <input className={styles.Input} /> */}
                <label className={styles.Label1} htmlFor="Label1">
                  Click the right button to upload file
                </label>
                <input type={"file"} className={styles.Button1} />
                <input type={"submit"} className={styles.Button2} />
              </div>
            </div>
          </div>
          <div className={styles.ContentRight}>
            <div className={styles.Logo2}>
              <Image
                className="max-w-xs h-auto"
                src={Logo2}
                alt="image description"
                height={700}
                width={700}
              />
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
function clsx(arg0: string): string | undefined {
  throw new Error("Function not implemented.");
}
