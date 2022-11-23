import React from "react";
import styles from "./Footer.module.scss";
import Image from "next/image";
import Logo from "@/assets/logo.svg";
export default function Footer() {
  return (
    <>
      <footer className="p-4 bg-white rounded-lg shadow md:px-6 md:py-4 dark:bg-gray-900">
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
