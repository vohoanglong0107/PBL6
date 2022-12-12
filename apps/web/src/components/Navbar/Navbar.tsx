import React from "react";
import Image from "next/image";
import Logo from "@/assets/logo.svg";

export default function Navbar() {
  return (
    <>
      <div className="flex items-center justify-between w-full px-3 py-3 mx-auto max-w-8xl lg:px-4">
        <div className="flex items-center">
          <button
            id="toggleSidebarMobile"
            aria-expanded="true"
            aria-controls="sidebar"
            className="p-2 mr-2 text-gray-600 rounded cursor-pointer lg:hidden hover:text-gray-900 hover:bg-gray-100 focus:bg-gray-100 dark:focus:bg-gray-700 focus:ring-2 focus:ring-gray-100 dark:focus:ring-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
          >
            <svg
              id="toggleSidebarMobileHamburger"
              className="w-6 h-6"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                clip-rule="evenodd"
              ></path>
            </svg>
            <svg
              id="toggleSidebarMobileClose"
              className="hidden w-6 h-6"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>
          <div
            className="flex items-center justify-between"
            style={{ marginLeft: "100px" }}
          >
            <a href="/" className="flex">
              <Image
                src={Logo}
                className="h-8 mr-3"
                alt="Music RegZ Logo"
                height={65}
                width={65}
              />
              <span
                className="self-center text-2xl font-semibold whitespace-nowrap "
                style={{ marginLeft: "15px", fontSize: "40px" }}
              >
                Music RegZ
              </span>
            </a>
          </div>
        </div>

        <div className="flex items-center" style={{ marginRight: "100px" }}>
          <ul
            id="musicRegMenu"
            className="flex-col hidden pt-6 lg:flex-row lg:self-center lg:py-0 lg:flex"
          >
            <li
              className="mb-3 lg:px-2 xl:px-2 lg:mb-0"
              style={{ marginRight: "15px", fontSize: "30px" }}
            >
              <a
                href="/"
                className="text-sm font-medium text-gray-900 hover:text-blue-600  dark:hover:text-blue-500"
              >
                Home
              </a>
            </li>
            <li
              className="mb-3 lg:px-2 xl:px-2 lg:mb-0"
              style={{ marginRight: "15px", fontSize: "30px" }}
            >
              <a
                href="/voicerecord"
                className="text-sm font-medium text-gray-900 hover:text-blue-600  dark:hover:text-blue-500"
              >
                Voice Record
              </a>
            </li>
            <li
              className="mb-3 lg:px-2 xl:px-2 lg:mb-0"
              style={{ marginRight: "15px", fontSize: "30px" }}
            >
              <a
                href="/supportlist"
                className="text-sm font-medium text-gray-900 hover:text-blue-600  dark:hover:text-blue-500"
              >
                Support List
              </a>
            </li>
            <li
              className="mb-3 lg:px-2 xl:px-2 lg:mb-0"
              style={{ marginRight: "15px", fontSize: "30px" }}
            >
              <a
                href="/aboutus"
                className="text-sm font-medium text-gray-900 hover:text-blue-600  dark:hover:text-blue-500"
              >
                About Us
              </a>
            </li>
            <li
              className="mb-3 lg:px-2 xl:px-2 lg:mb-0"
              style={{ marginRight: "15px", fontSize: "30px" }}
            >
              <a
                href="/contact/"
                className="text-sm font-medium text-gray-900 hover:text-blue-600  dark:hover:text-blue-500"
              >
                Contact
              </a>
            </li>
          </ul>
          <a
            href="https://github.com/vohoanglong0107/PBL6"
            data-tooltip-target="tooltip-github-2"
            className="hidden sm:inline-block text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5 mr-1"
          >
            <svg
              className="w-5 h-5"
              aria-hidden="true"
              focusable="false"
              data-prefix="fab"
              data-icon="github"
              role="img"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 496 512"
            >
              <path
                fill="currentColor"
                d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"
              ></path>
            </svg>
            <span className="sr-only">View on Github</span>
          </a>
          <div
            id="tooltip-github-2"
            role="tooltip"
            className="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip"
            style={{
              position: "absolute",
              inset: "auto auto 0px 0px",
              margin: "0px",
              transform: "translate3d(1098.4px, -61.6px, 0px)",
            }}
            data-popper-placement="top"
          >
            View on Github
            <div
              className="tooltip-arrow"
              data-popper-arrow=""
              style={{
                position: "absolute",
                left: "0px",
                transform: "translate3d(59.2px, 0px, 0px)",
              }}
            ></div>
          </div>
          <button
            id="theme-toggle"
            data-tooltip-target="tooltip-toggle"
            type="button"
            className="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5"
          >
            <svg
              aria-hidden="true"
              id="theme-toggle-dark-icon"
              className="w-5 h-5"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
            </svg>
            <svg
              aria-hidden="true"
              id="theme-toggle-light-icon"
              className="hidden w-5 h-5"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                fill-rule="evenodd"
                clip-rule="evenodd"
              ></path>
            </svg>
            <span className="sr-only">Toggle dark mode</span>
          </button>
          <div
            id="tooltip-toggle"
            role="tooltip"
            className="absolute z-10 inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm tooltip opacity-0 invisible"
            style={{
              position: "absolute",
              inset: "auto auto 0px 0px",
              margin: "0px",
              transform: "translate3d(1229.6px, -61.6px, 0px)",
            }}
            data-popper-placement="top"
          >
            Toggle dark mode
            <div
              className="tooltip-arrow"
              data-popper-arrow=""
              style={{
                position: "absolute",
                left: "0px",
                transform: "translate3d(68.8px, 0px, 0px)",
              }}
            ></div>
          </div>
          <a
            href="/pro/#pricing"
            className="xl:hidden inline-flex items-center text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center ml-3"
          >
            Pricing
          </a>
          <a
            href="/pro/#pricing"
            className="hidden xl:inline-flex items-center text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center ml-3"
          >
            Pricing &amp; FAQ
          </a>
        </div>
      </div>
    </>
  );
}
