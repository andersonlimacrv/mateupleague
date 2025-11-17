export interface ApiUser {
  id: number;
  username: string;
  email: string;
  role?: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
  avatarUrl?: string;
}

export interface CreateUserDTO {
  username: string;
  email: string;
  password: string;
  role?: string;
  avatarUrl?: string;
}

export interface UpdateUserDTO {
  username?: string;
  email?: string;
  password?: string;
  role?: string;
  avatarUrl?: string;
  is_active?: boolean;
}
