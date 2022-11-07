import React from "react";
import styles from "./SongSearchForm.module.scss";
export default function SongSearchForm() {
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

          <div className={styles.UploadFile}>
            <label className={styles.Label1} htmlFor="Label1">
              Click the right button to upload file
            </label>
            <input type={"file"} className={styles.Button1} />
            <input type={"submit"} className={styles.Button2} />
          </div>
        </div>
      </div>
    </>
  );
}
function clsx(arg0: string): string | undefined {
  throw new Error("Function not implemented.");
}
