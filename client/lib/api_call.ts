import axios from "axios";
import { JWT } from "./jwt";

const instance = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_API_URL}/api`,
  timeout: 20000, // Set timeout to 10 seconds
});

instance.interceptors.request.use(
  async function (config) {
    const token = JWT.getAccessToken() ?? "";

    if (token) config["headers"]["Authorization"] = `Bearer ${token}`;

    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

export const axiosInstance = instance;

export const apiGET = (url: string, params?: any) =>
  instance
    .get(url, {
      params: params,
    })
    .then((res) => res.data);

export const apiPOST = async (url: string, { arg }: { arg: any }) =>
  instance.post(url, arg).then((res) => res.data);

export const apiPlainPOST = async (url: string, { arg }: { arg: any }) =>
  instance.post(url, arg).then((res) => res);

export const apiPATCH = async (url: string, { arg }: { arg: any }) =>
  instance.patch(url, arg).then((res) => res.data);

// export const apiPATCH = (url: string, { args }: { args: any }) =>
//   instance.patch(url, args).then((res) => res.data);

export const apiDELETE = (url: string, { args }: { args: any }) =>
  instance.delete(url, args).then((res) => res.data);
