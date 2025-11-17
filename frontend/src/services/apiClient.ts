import axios from "axios";
import { API_URL } from "@/lib/constants";

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const setAccessToken = (token: string) => {
  localStorage.setItem("access_token", token);
};

export const getAccessToken = (): string | null => {
  return localStorage.getItem("access_token");
};

export const clearAccessToken = () => {
  localStorage.removeItem("access_token");
};

apiClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const logoutEvent = new CustomEvent("auth:unauthorized");
      window.dispatchEvent(logoutEvent);
    }
    return Promise.reject(error);
  }
);

export default apiClient;
