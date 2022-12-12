import React from "react";
import Nam from "@/assets/nam.jpg";
import Long from "@/assets/long.jpg";
import Huy from "@/assets/huy.jpg";
import Image from "next/image";
import styles from "./AboutUs.module.scss";

export default function AboutUs() {
  return (
    <>
      <div className={styles.AboutUs}>
        <div className=" max-w-sm mt-5 bg-blue-300 rounded-lg border border-gray-800 shadow-md dark:bg-gray-800 dark:border-gray-700 hover:bg-blue-500 ">
          <a href="#">
            <Image className={styles.avt} src={Long} alt="namphoto" />
          </a>
          <div className="p-5">
            <a href="#">
              <h5 className="mb-2 text-3xl font-bold tracking-tight text-gray-900 dark:text-white md:text-center">
                Vo Hoang Long
              </h5>
            </a>
            <p className="mb-3 font-normal text-gray-700 dark:text-gray-400 md:text-center">
              Team Leader
            </p>
            <p className="mb-3 font-normal text-gray-700 dark:text-gray-400 md:text-center">
              19TCLC_Nhat2
            </p>
          </div>
        </div>

        <div className=" max-w-sm mt-5 ml-10 bg-blue-300 rounded-lg border border-gray-800 shadow-md dark:bg-gray-800 dark:border-gray-700 hover:bg-blue-500">
          <a href="#">
            <Image className={styles.avt} src={Huy} alt="namphoto" />
          </a>
          <div className="p-5">
            <a href="#">
              <h5 className="mb-2 text-3xl font-bold tracking-tight text-gray-900 dark:text-white md:text-center">
                Nguyen Ngoc Huy
              </h5>
            </a>
            <p className="mb-3 font-normal text-gray-700 dark:text-gray-400 md:text-center">
              Team Member
            </p>
            <p className="mb-3 font-normal text-gray-700 dark:text-gray-400 md:text-center">
              19TCLC_Nhat2
            </p>
          </div>
        </div>

        <div className=" max-w-sm mt-5 ml-10 bg-blue-300 rounded-lg border border-gray-800 shadow-md dark:bg-gray-800 dark:border-gray-700 hover:bg-blue-500">
          <a href="#">
            <Image className={styles.avt} src={Nam} alt="namphoto" />
          </a>
          <div className="p-5">
            <a href="#">
              <h5 className="mb-2 text-3xl font-bold tracking-tight text-gray-900 dark:text-white md:text-center">
                Nguyen Duc Nam
              </h5>
            </a>
            <p className="mb-3 font-normal text-gray-700 dark:text-gray-400 md:text-center">
              Team Member
            </p>
            <p className="mb-3 font-normal text-gray-700 dark:text-gray-400 md:text-center">
              19TCLC_Nhat2
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
