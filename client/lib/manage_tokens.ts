"use client";
import { axiosInstance } from "./api_call";

export const refreshAccessToken = async () => {
  const refresh = localStorage.getItem("refresh");
  if (!refresh) return null;

  try {
    const res = await axiosInstance.post("api/token/refresh/", {
      refresh,
    });

    localStorage.setItem("access", res.data.access);
    return res.data.access;
  } catch (err) {
    console.error("Refresh token expired", err);
    localStorage.clear();
    return null;
  }
};

export const logout = async () => {
  // const router = useRouter();
  // localStorage.clear();
  // router.push("/login");
};
