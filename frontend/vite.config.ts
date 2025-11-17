// vite.config.ts
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { visualizer } from "rollup-plugin-visualizer";
import tailwindcss from "@tailwindcss/vite";
import path from "node:path";

export default defineConfig(({ mode }) => {
  // 1. Lê todas as variáveis do .env (VITE_… incluídas)
  const env = loadEnv(mode, process.cwd(), "VITE_");

  const frontendPort = Number(env.VITE_FRONTEND_PORT);
  const backendPort = Number(env.VITE_BACKEND_PORT);
  const backendUrl = `http://localhost:${backendPort}`;

  console.log(`⚡ Frontend: http://localhost:${frontendPort}`);
  console.log(`🐍 Backend : ${backendUrl}`);
  console.log(`🦟 Broker API: ${env.VITE_BROKER_API_URL}`);

  return {
    plugins: [
      react(),
      tailwindcss(),
      visualizer({
        open: true,
        filename: "bundle-stats.html",
        template: "sunburst",
        gzipSize: true,
        brotliSize: true,
      }),
    ],

    resolve: {
      alias: { "@": path.resolve(__dirname, "src") },
    },

    build: {
      outDir: "dist",
      emptyOutDir: true,
      chunkSizeWarningLimit: 800,
    },

    server: {
      port: frontendPort,
      proxy: {
        "/api": {
          target: backendUrl,
          changeOrigin: true,
          rewrite: (p) => p.replace(/^\/api/, ""),
        },
      },
    },
  };
});
