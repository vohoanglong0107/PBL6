import React from "react";
import classNames from "classnames";
import styles from "./Banner.module.scss";
import Image from "next/image";
import Logo2 from "@/assets/logo2.svg";
import Head from "next/head";

export default function Banner() {
  return (
    <Image
      className="max-w-xs h-auto"
      src={Logo2}
      alt="image description"
      height={700}
      width={700}
    />
  );
}
