import React from "react";
import classNames from "classnames";
import styles from "./HelloWorld.module.scss";
export default function HelloWorld() {
  return (
    <h1
      className={classNames(
        styles["hello-world"],
        "text-3xl",
        "font-bold",
        "underline"
      )}
    >
      Hello World!
    </h1>
  );
}
