import styles from "./ShowResult.module.scss";
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
  const max5Results = useMemo(() => results.slice(0, 5), [results]);
  return (
    <>
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
    </>
  );
}
