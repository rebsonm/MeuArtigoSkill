import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [viteSingleFile()],
  build: { rollupOptions: { input: "mcp-app.html" }, outDir: "dist", emptyOutDir: false },
});
