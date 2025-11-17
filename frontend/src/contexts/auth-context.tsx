import {
  createContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import type { AuthContextType, User } from "@/types/auth";
import { usersApi } from "@/services/domains/users/usersApi";
import { useToast } from "@/hooks/useToast";
const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

const AuthProvider = ({ children }: AuthProviderProps) => {
  const { addToast } = useToast();
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem("access_token")
  );
  const [user, setUser] = useState<User | null>(() => {
    const savedUser = localStorage.getItem("user");
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [isLoading, setIsLoading] = useState(false);

  const login = async (userData: User, token: string) => {
    setIsLoading(true);
    try {
      setToken(token);
      setUser(userData);
      localStorage.setItem("access_token", token);
      localStorage.setItem("user", JSON.stringify(userData));
      addToast({
        type: "success",
        title: "Login successful!",
        description: `Welcome, ${userData.username}!`,
      });
    } finally {
      setIsLoading(false);
    }
  };
  const clearAuth = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
  };

  const logout = useCallback(async () => {
    setIsLoading(true);
    try {
      await usersApi.logout();
    } finally {
      clearAuth();
      setIsLoading(false);
    }
  }, []);

  const getAuthHeader = () =>
    token ? { Authorization: `Bearer ${token}` } : null;

  const isAuthenticated = !!token;

  useEffect(() => {
    const handleUnauthorized = () => {
      clearAuth();

      addToast({
        type: "error",
        title: "Session Expired.",
        description: "Your session has expired. Please log in again.",
      });
    };

    window.addEventListener("auth:unauthorized", handleUnauthorized);

    return () => {
      window.removeEventListener("auth:unauthorized", handleUnauthorized);
    };
  }, [addToast]);

  useEffect(() => {
    const syncAuth = (e: StorageEvent) => {
      if (e.key === "access_token") {
        setToken(e.newValue);
      }
      if (e.key === "user") {
        setUser(e.newValue ? JSON.parse(e.newValue) : null);
      }
    };
    window.addEventListener("storage", syncAuth);
    return () => window.removeEventListener("storage", syncAuth);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated, isLoading, login, logout, getAuthHeader }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
