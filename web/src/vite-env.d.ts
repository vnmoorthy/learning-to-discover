/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_STATIC?: string
  readonly VITE_FIXTURES?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
