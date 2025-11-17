import React, { createContext } from "react";
import { toast, Toaster } from "sonner";

interface ToastContextType {
  addToast: (options: {
    type: "success" | "error" | "info" | "warning";
    title: string;
    description?: string;
    duration?: number;
  }) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const addToast = ({
    type,
    title,
    description,
    duration = 3000,
  }: {
    type: "success" | "error" | "info" | "warning";
    title: string;
    description?: string;
    duration?: number;
  }) => {
    const getIcon = () => {
      switch (type) {
        case "success":
          return (
            <svg
              className="w-5 h-5 text-green-500"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
                fill="currentColor"
              />
            </svg>
          );
        case "error":
          return (
            <svg
              className="w-5 h-5 text-red-500"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"
                fill="currentColor"
              />
            </svg>
          );
        case "warning":
          return (
            <svg
              className="w-5 h-5 text-yellow-500"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"
                fill="currentColor"
              />
            </svg>
          );
        default:
          return (
            <svg
              className="w-5 h-5 text-blue-500"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
                fill="currentColor"
              />
            </svg>
          );
      }
    };

    const toastOptions = {
      duration,
      icon: getIcon(),
      description,
      action: {
        label: (
          <svg
            className="w-4 h-4"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M18 6L6 18M6 6l12 12"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        ),
        onClick: () => {},
      },
      className: "sonner-toast",
    };

    switch (type) {
      case "success":
        toast.success(title, toastOptions);
        break;
      case "error":
        toast.error(title, toastOptions);
        break;
      case "warning":
        toast.warning(title, toastOptions);
        break;
      default:
        toast.info(title, toastOptions);
        break;
    }
  };

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      <Toaster
        position="top-center"
        expand={true}
        richColors={true}
        closeButton={false}
        toastOptions={{
          className: "sonner-toast",
          style: {
            background: "rgba(255, 255, 255, 0.1)",
            backdropFilter: "blur(16px)",
            border: "1px solid rgba(255, 255, 255, 0.2)",
            borderRadius: "12px",
            color: "hsl(var(--foreground))",
            fontSize: "14px",
            fontWeight: "500",
            padding: "4px",
            boxShadow: "0 8px 32px rgba(0, 0, 0, 0.1)",
          },
        }}
        theme="system"
      />
    </ToastContext.Provider>
  );
}

export { ToastContext };
