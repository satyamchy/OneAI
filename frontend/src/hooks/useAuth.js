import { useEffect, useState } from 'react';
import { getMe, loginUser, registerUser } from '../api/authApi.js';

// Manages JWT-backed auth state for pages and route guards.
export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Validates the stored token when the hook first mounts.
  useEffect(() => {
    const token = localStorage.getItem('paios_token');
    if (!token) {
      setLoading(false);
      return;
    }
    getMe()
      .then((data) => setUser(data.user))
      .catch(() => localStorage.removeItem('paios_token'))
      .finally(() => setLoading(false));
  }, []);

  // Logs in and stores the returned JWT.
  async function login(payload) {
    const data = await loginUser(payload);
    localStorage.setItem('paios_token', data.access_token);
    setUser(data.user);
    return data.user;
  }

  // Registers and stores the returned JWT.
  async function register(payload) {
    const data = await registerUser(payload);
    localStorage.setItem('paios_token', data.access_token);
    setUser(data.user);
    return data.user;
  }

  // Clears the local session.
  function logout() {
    localStorage.removeItem('paios_token');
    setUser(null);
  }

  return { user, loading, login, register, logout };
}
