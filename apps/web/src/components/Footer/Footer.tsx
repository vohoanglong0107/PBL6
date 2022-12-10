import React from "react";
import styles from "./Footer.module.scss";
import Image from "next/image";
import Logo from "@/assets/logo.svg";
export default function Footer() {
  return (
    <>
      <footer className="fixed bottom-0 left-0 z-20 w-full bg-white border-t border-gray-200 shadow md:flex md:items-center md:justify-between  dark:bg-gray-800 dark:border-gray-600 pr-10">
        <div className="sm:flex sm:items-center sm:justify-between"></div>
        <hr className="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8" />
        <span className="block text-sm text-gray-500 sm:text-center dark:text-gray-400">
          © 2022{" "}
          <a href="https://flowbite.com/" className="hover:underline">
            Music RegZ™
          </a>
          . All Rights Reserved.
        </span>
      </footer>
    </>
  );
}
function clsx(arg0: string): string | undefined {
  throw new Error("Function not implemented.");
}
