import React from "react";
import classNames from "classnames";
import styles from "./Banner.module.scss";
import Image from "next/image";
import Avt from "@/assets/avt.jpg";
import Head from "next/head";

export default function Banner(){
    return(
        <>
        
          <Image
            className="max-w-xs h-auto"
            src={Avt}
            alt="image description"
            height={500}
            width={400}
          />
       
        </>

    )
        
}
