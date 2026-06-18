# Frontend Setup Notes

This frontend is React JavaScript with Vite, Tailwind CSS, React Router v6, Axios, Zustand, react-markdown, and react-syntax-highlighter.

## Install Later

From `paios/frontend`:

```bash
npm install
```

## Run Later

```bash
npm run dev
```

## Frontend Structure

- `src/api`: Axios client and backend API wrappers.
- `src/pages`: route-level login, register, and chat pages.
- `src/components/sidebar`: conversation list and mode icons.
- `src/components/mode`: top-center interaction mode selector.
- `src/components/chat`: messages, markdown rendering, composer, sources, tools.
- `src/components/run-details`: run metadata panel.
- `src/hooks`: auth lifecycle hook.
- `src/store`: Zustand state stores for later expansion.
- `src/routes`: route guards and route helpers.
