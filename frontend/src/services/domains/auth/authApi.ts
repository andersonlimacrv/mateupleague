/* /service/domains/authApi.ts */

import apiClient, { setAccessToken } from "@/services/apiClient";

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface UserData {
  id: number;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  update_at: string;
}

export const login = async (
  username: string,
  password: string
): Promise<LoginResponse> => {
  const body = new URLSearchParams({
    grant_type: "password",
    username,
    password,
  });

  const response = await apiClient.post<LoginResponse>("/auth/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  setAccessToken(response.data.access_token); //
  return response.data;
};

export const getCurrentUser = async (): Promise<UserData> => {
  const response = await apiClient.get<UserData>("/users/me");
  return response.data;
};
