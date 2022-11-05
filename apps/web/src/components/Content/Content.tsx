import React from "react";
import styles from "./Content.module.scss";
import Image from "next/image";
import Logo2 from "@/assets/logo2.svg";
import Navbar from "../Navbar";
import Banner from "../Banner";
import SongSearchForm from "../SongSearchForm";
export default function Content() {
  return (
    <>
      <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
      ></meta>
      <br />
      <section className={styles.Section}>
        <div className={styles.Content}>
          <SongSearchForm />
          <div className={styles.ContentRight}>
            <div className={styles.Logo2}>
              <Banner />
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
