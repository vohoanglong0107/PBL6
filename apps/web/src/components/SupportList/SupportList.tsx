import React, { useEffect, useState, useRef } from "react";
import axios from "@/api/axios";
const getListSong = () => axios.get("/songs");

export default function SupportList() {
  const [Songs, setSongs] = useState<any[]>([]);
  const [query, setQuery] = useState("");
  const search = (data: any) => {
    return data.filter(
      (item: any) =>
        item.title.toLowerCase().includes(query.toLowerCase()) ||
        item.artist.toLowerCase().includes(query.toLowerCase())
    );
  };
  const fetchSong = async () => {
    try {
      await getListSong().then((res: any) => {
        console.log(res);
        console.log(res.data);
        setSongs(
          res.data.map((data: any) => {
            return {
              id: data.id,
              artist: data.artist,
              title: data.title,
              url: data.url,
            };
          })
        );
      });
    } catch (error) {
      console.log(error);
    }
  };
  useEffect(() => {
    fetchSong();
  }, []);

  const numAscending = [...Songs].sort((a, b) => (a.title > b.title ? 1 : -1));

  return (
    <>
      <div className="overflow-x-auto my-8 mx-4 relative shadow-md sm:rounded-lg">
        <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
          <caption className="p-5 text-lg font-semibold text-left text-gray-900 bg-white dark:text-white dark:bg-gray-800">
            Our Support Audio List
            <p className="mt-1 mb-5 text-sm font-normal text-gray-500 dark:text-gray-400">
              We cannot provide service to all songs, but you can check if the
              song you are looking for is supported in this list by typing the
              title, or artist in the search field below. The list of supported
              songs will be updated regularly.
            </p>
            <form className="flex items-center">
              <label htmlFor="simple-search" className="sr-only">
                Search
              </label>
              <div className="relative w-full">
                <div className="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
                  <svg
                    aria-hidden="true"
                    className="w-5 h-5 text-gray-500 dark:text-gray-400"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                </div>
                <input
                  type={"text"}
                  id="simple-search"
                  className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder="Songs, Artists"
                  required
                  onChange={(e) => setQuery(e.target.value)}
                />
              </div>
              <button
                type="submit"
                className="p-2.5 ml-2 text-sm font-medium text-white bg-blue-700 rounded-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  ></path>
                </svg>
                <span className="sr-only">Search</span>
              </button>
            </form>
          </caption>

          <thead className="text-lg text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400 text-center">
            <tr>
              <th scope="col" className="py-4 px-6">
                Order
              </th>
              <th scope="col" className="py-4 px-6">
                Song Name
              </th>
              <th scope="col" className="py-4 px-6">
                Artist
              </th>
            </tr>
          </thead>

          <tbody>
            {search(numAscending).map((data: any, index: any) => (
              <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 text-center">
                <th
                  scope="row"
                  className="py-4 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white text-sm "
                >
                  {index + 1}
                </th>
                <td className="py-4 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white text-sm">
                  {data.title}
                </td>
                <td className="py-4 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white text-sm">
                  {data.artist}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
