import { Navigate, Route, Routes } from "react-router-dom";

import { LoginPage } from "./features/auth/LoginPage.jsx";
import { RegisterPage } from "./features/auth/RegisterPage.jsx";
import { ChatPage } from "./features/chat/ChatPage.jsx";
import { SettingsPage } from "./features/settings/SettingsPage.jsx";
import { useAuthStore } from "./stores/authStore.js";

function ProtectedRoute({ children }) {
  //const token = useAuthStore((state) => state.token);
  // if (!token) {
  //   return <Navigate to="/login" replace />;
  // }
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <ChatPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <SettingsPage />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

