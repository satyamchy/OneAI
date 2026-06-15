import { Link } from "react-router-dom";

import { Button } from "../../components/ui/Button.jsx";
import { useAuthStore } from "../../stores/authStore.js";

export function SettingsPage() {
  const user = useAuthStore((state) => state.user);
  const clearSession = useAuthStore((state) => state.clearSession);

  return (
    <main className="min-h-screen bg-stone-100 p-6">
      <section className="mx-auto max-w-2xl rounded-lg border border-stone-200 bg-white p-6 shadow-panel">
        <h1 className="text-xl font-semibold text-stone-950">Settings</h1>
        <div className="mt-5 space-y-2 text-sm text-stone-600">
          <p>Email: {user?.email}</p>
          <p>Default model: {user?.default_model_id || "Platform default"}</p>
        </div>
        <div className="mt-6 flex gap-2">
          <Link to="/">
            <Button variant="secondary">Back</Button>
          </Link>
          <Button variant="danger" onClick={clearSession}>
            Sign out
          </Button>
        </div>
      </section>
    </main>
  );
}

