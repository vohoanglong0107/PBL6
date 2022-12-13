import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "https://songs-uploader.pbl6.mamlong34.monster/api",
});

export default axiosInstance;
