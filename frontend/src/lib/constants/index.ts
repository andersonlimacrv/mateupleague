const MODE = import.meta.env.MODE;
const backendUrl = import.meta.env.VITE_DEPLOY_API;

const port = Number(import.meta.env.VITE_BACKEND_PORT) || 3000;

export const API_URL =
  MODE === "production" ? backendUrl : `http://localhost:${port}`;
