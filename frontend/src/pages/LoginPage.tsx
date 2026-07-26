import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { Icon } from "@/components/ui/Icon";
import kspLogo from "@/assets/Karnataka Police.svg";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(username, password);
      navigate("/dashboard");
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Invalid username or password.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="flex flex-col min-h-screen items-center justify-center p-4 bg-surface relative">
      <div className="fixed inset-0 pointer-events-none opacity-[0.03] overflow-hidden">
        <div
          className="absolute inset-0"
          style={{ backgroundImage: "radial-gradient(#0b1f5e 1px, transparent 1px)", backgroundSize: "32px 32px" }}
        />
      </div>

      <main className="w-full max-w-[440px] z-10">
        <div className="bg-surface-container-lowest rounded-xl p-6 flex flex-col items-center border border-card-border shadow-sm">
          <div className="mb-6 flex flex-col items-center text-center">
            <div className="w-24 h-24 mb-4 flex items-center justify-center">
              <img src={kspLogo} alt="Karnataka Police Logo" className="w-full h-full object-contain drop-shadow-md" />
            </div>
            <h1 className="text-2xl font-semibold text-on-background mb-1">Karnataka Police</h1>
            <p className="text-sm text-on-surface-variant">KSP Crime AI</p>
          </div>

          <form onSubmit={handleSubmit} className="w-full space-y-6">
            <div className="space-y-2">
              <label className="text-[11px] font-semibold tracking-wide uppercase text-on-surface-variant block" htmlFor="username">
                Username
              </label>
              <div className="relative">
                <Icon name="badge" className="absolute left-4 top-1/2 -translate-y-1/2 text-outline text-xl" />
                <input
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter username"
                  required
                  className="w-full pl-12 pr-4 py-3 bg-surface-container-low border border-outline-variant rounded-lg text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary-container transition-all"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-[11px] font-semibold tracking-wide uppercase text-on-surface-variant block" htmlFor="password">
                Password
              </label>
              <div className="relative">
                <Icon name="lock" className="absolute left-4 top-1/2 -translate-y-1/2 text-outline text-xl" />
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="w-full pl-12 pr-4 py-3 bg-surface-container-low border border-outline-variant rounded-lg text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary-container transition-all"
                />
              </div>
            </div>

            {error && (
              <div className="flex items-center gap-2 px-3 py-2 bg-error-container/40 border border-error/30 rounded-lg text-error text-sm">
                <Icon name="error" className="text-base" />
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-primary-container text-on-primary py-3 rounded-lg font-bold text-sm flex items-center justify-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-60 shadow-sm"
            >
              {submitting ? (
                <>
                  <Icon name="progress_activity" className="animate-spin text-lg" />
                  Verifying Credentials...
                </>
              ) : (
                <>
                  Login
                </>
              )}
            </button>

            <p className="text-center text-sm text-on-surface-variant">
              New officer?{" "}
              <Link to="/register" className="text-primary font-semibold hover:underline">
                Register for access
              </Link>
            </p>
          </form>
        </div>


      </main>
    </div>
  );
}
