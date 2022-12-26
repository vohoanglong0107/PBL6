import styles from "./ShowResult.module.scss";
import { useRouter } from "next/router";
import React, { useMemo } from "react";

interface Result {
  artist: string;
  id: string;
  title: string;
}

interface Props {
  results: Result[];
}

export default function ShowResult({ results }: Props) {
  const router = useRouter();
  const handleClick = (e: any) => {
    router.push({
      pathname: "/",
    });
  };
  const max5Results = useMemo(() => results.slice(0, 5), [results]);
  return (
    <>
      <div>
        <section className={styles.Section}>
          <div className={styles.Content}>
            <div className={styles.info_song}>
              <div className={styles.info}>
                <div className={styles.songs}>
                  <h5 className={styles.song}>Song</h5>
                  {max5Results.map((result, index) => (
                    <p
                      key={result.id}
                      className={styles[`sub_song_name${index}`]}
                    >
                      {result.title}
                    </p>
                  ))}
                </div>
                <div className={styles.artists}>
                  <h5 className={styles.artist}>Artist</h5>
                  {max5Results.map((result, index) => (
                    <p
                      key={result.id}
                      className={styles[`sub_artist_name${index}`]}
                    >
                      {result.artist}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>
        <div className="container py-50 px-10 mx-0 min-w-full flex flex-col items-center ">
          <button
            type="button"
            onClick={handleClick}
            className="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center  mr-2 mb-2"
          >
            Can{"'"}t find the song? Try again
          </button>
        </div>
      </div>
    </>
  );
}
