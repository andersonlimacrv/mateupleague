import { AxiosError } from "axios";

type ValidationErrorDetail = {
  loc?: (string | number)[];
  msg: string;
  type?: string;
  input?: unknown;
};

type ApiErrorResponse = {
  detail?: string | ValidationErrorDetail[];
  message?: string;
};

export function getApiErrorMessage(error: unknown): string {
  const axiosError = error as AxiosError<ApiErrorResponse>;

  const data = axiosError.response?.data;
  const status = axiosError.response?.status;

  // Erro 422 - Validação
  if (status === 422 && Array.isArray(data?.detail)) {
    return data.detail
      .map((d) => {
        const field = d.loc?.slice(-1)[0] ?? "campo";
        return `${field}: ${d.msg}`;
      })
      .join("\n");
  }

  if (status === 400) {
    if (typeof data?.detail === "string") {
      return data.detail;
    }
    if (Array.isArray(data?.detail)) {
      return data.detail
        .map((d) => {
          const field = d.loc?.slice(-1)[0] ?? "campo";
          return `${field}: ${d.msg}`;
        })
        .join("\n");
    }
    if (data?.message) {
      return data.message;
    }
    return "Bad Request - An error occurred while processing the request.";
  }

  if (typeof data?.detail === "string") {
    return data.detail;
  }

  if (data?.message) {
    return data.message;
  }

  return "👀 Ooops! Something went wrong. Try again later.";
}
