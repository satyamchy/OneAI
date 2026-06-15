import { Link, useNavigate } from "react-router-dom";

import { Button } from "../../components/ui/Button.jsx";
import { ErrorState } from "../../components/ui/ErrorState.jsx";
import { Input } from "../../components/ui/Input.jsx";
import { AuthLayout } from "../../layouts/AuthLayout.jsx";
import { useAuthStore } from "../../stores/authStore.js";
import { useLoginMutation } from "./authHooks.js";

export function LoginPage() {
  const navigate = useNavigate();
  const setSession = useAuthStore((state) => state.setSession);
  const mutation = useLoginMutation();

  async function handleSubmit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const session = await mutation.mutateAsync({
      email: form.get("email"),
      password: form.get("password")
    });
    setSession(session);
    navigate("/");
  }

  return (
    <AuthLayout title="OneAI" subtitle="Sign in to your local chat core.">
      <form className="space-y-4" onSubmit={handleSubmit}>
        {mutation.error ? <ErrorState message={mutation.error.message} /> : null}
        <Input name="email" type="email" placeholder="Email" required />
        <Input name="password" type="password" placeholder="Password" required />
        <Button className="w-full" disabled={mutation.isPending}>
          Sign in
        </Button>
      </form>
      <p className="mt-5 text-center text-sm text-stone-500">
        No account yet?{" "}
        <Link className="font-medium text-emerald-700" to="/register">
          Create one
        </Link>
      </p>
    </AuthLayout>
  );
}

