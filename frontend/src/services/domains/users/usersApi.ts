import apiClient from "@/services/apiClient";
import type { ApiUser, CreateUserDTO, UpdateUserDTO } from "@/types/user";

export const usersApi = {
  getAll: async (): Promise<{ users: ApiUser[] }> => {
    const res = await apiClient.get<{ users: ApiUser[] }>("/users");
    return res.data;
  },

  getById: async (id: number): Promise<ApiUser> => {
    const res = await apiClient.get<ApiUser>(`/users/${id}`);
    return res.data;
  },

  create: async (data: CreateUserDTO): Promise<ApiUser> => {
    const res = await apiClient.post<ApiUser>("/users", data);
    return res.data;
  },

  update: async (id: number, data: UpdateUserDTO): Promise<ApiUser> => {
    const res = await apiClient.put<ApiUser>(`/users/${id}`, data);
    return res.data;
  },

  deleteById: async (id: number): Promise<void> => {
    await apiClient.delete(`/users/${id}`);
  },

  activateOrDeactivate: async (
    id: number
  ): Promise<{ is_active: boolean; update_at: string }> => {
    const res = await apiClient.put<{ is_active: boolean; update_at: string }>(
      `/users/${id}/allow`
    );
    return res.data;
  },

  getStats: async (): Promise<{
    total_users: number;
    active_users: number;
    inactive_users: number;
    users_by_role: Record<string, number>;
    recent_logins: number;
    active_sessions: number;
    total_sessions_today: number;
    unique_users_today: number;
    average_session_duration: number;
  }> => {
    const res = await apiClient.get<{
      total_users: number;
      active_users: number;
      inactive_users: number;
      users_by_role: Record<string, number>;
      recent_logins: number;
      active_sessions: number;
      total_sessions_today: number;
      unique_users_today: number;
      average_session_duration: number;
    }>("/users/session/stats");
    return res.data;
  },

  logout: async (): Promise<{ message: string }> => {
    const res = await apiClient.post<{ message: string }>("/auth/logout");
    return res.data;
  },
};
