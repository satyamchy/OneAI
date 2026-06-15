import { Link, useNavigate } from "react-router-dom";

import { Button } from "../../components/ui/Button.jsx";
import { ErrorState } from "../../components/ui/ErrorState.jsx";
import { Input } from "../../components/ui/Input.jsx";
import { AuthLayout } from "../../layouts/AuthLayout.jsx";
import { useAuthStore } from "../../stores/authStore.js";
import { useRegisterMutation } from "./authHooks.js";

export function RegisterPage() {
  const navigate = useNavigate();
  const setSession = useAuthStore((state) => state.setSession);
  const mutation = useRegisterMutation();

  async function handleSubmit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const session = await mutation.mutateAsync({
      display_name: form.get("display_name"),
      email: form.get("email"),
      password: form.get("password")
    });
    setSession(session);
    navigate("/");
  }

  return (
    <AuthLayout title="Create OneAI" subtitle="Start with the Phase 1 chat core.">
      <form className="space-y-4" onSubmit={handleSubmit}>
        {mutation.error ? <ErrorState message={mutation.error.message} /> : null}
        <Input name="display_name" placeholder="Display name" />
        <Input name="email" type="email" placeholder="Email" required />
        <Input name="password" type="password" placeholder="Password" minLength={8} required />
        <Button className="w-full" disabled={mutation.isPending}>
          Create account
        </Button>
      </form>
      <p className="mt-5 text-center text-sm text-stone-500">
        Already have an account?{" "}
        <Link className="font-medium text-emerald-700" to="/login">
          Sign in
        </Link>
      </p>
    </AuthLayout>
  );
}

