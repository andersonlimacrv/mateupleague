export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  update_at: string;
  avatar_url?: string;
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (userData: User, token: string) => Promise<void>; // Assinatura atualizada
  logout: () => void;
  getAuthHeader: () => { Authorization: string } | null;
}
