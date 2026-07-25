import { useState } from "react";
import { Link } from "react-router-dom";
import { register as apiRegister } from "@/api/auth";
import { Icon } from "@/components/ui/Icon";
import { ROLES } from "@/types/roles";

// Admin (R1) is never self-registrable — only an existing admin can
// create another admin account (see UsersPage.tsx). Mirrors the backend
// check in api/routes/auth.py (NON_SELF_REGISTRABLE_ROLES).
const SELF_REGISTRABLE_ROLES = Object.values(ROLES).filter((r) => r.role_id !== "R1");

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [roleId, setRoleId] = useState(SELF_REGISTRABLE_ROLES[SELF_REGISTRABLE_ROLES.length - 1]?.role_id ?? "R6");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setSubmitting(true);
    try {
      await apiRegister(username, password, roleId);
      setSubmitted(true);
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Could not submit registration. Please try again.");
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
            <div className="w-16 h-16 mb-4 rounded-full bg-primary-container flex items-center justify-center">
              <Icon name="person_add" className="text-on-primary text-4xl" filled />
            </div>
            <h1 className="text-2xl font-semibold text-on-background mb-1">Officer Registration</h1>
            <p className="text-sm text-on-surface-variant">KSP Crime AI</p>
          </div>

          {submitted ? (
            <div className="w-full flex flex-col items-center text-center gap-4 py-4">
              <Icon name="hourglass_top" className="text-primary text-4xl" />
              <div>
                <h2 className="text-base font-semibold text-on-surface mb-1">Registration submitted</h2>
                <p className="text-sm text-on-surface-variant">
                  Your account has been created and is <span className="font-semibold">pending admin approval</span>.
                  You'll be able to log in once an administrator reviews and approves your request.
                </p>
              </div>
              <Link
                to="/login"
                className="w-full bg-primary-container text-on-primary py-3 rounded-lg font-bold text-sm flex items-center justify-center gap-2 hover:opacity-90 transition-opacity shadow-sm"
              >
                Back to Login
                <Icon name="arrow_forward" className="text-lg" />
              </Link>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="w-full space-y-5">
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
                    placeholder="Choose a username"
                    required
                    minLength={3}
                    className="w-full pl-12 pr-4 py-3 bg-surface-container-low border border-outline-variant rounded-lg text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary-container transition-all"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-[11px] font-semibold tracking-wide uppercase text-on-surface-variant block" htmlFor="role">
                  Requested Role
                </label>
                <div className="relative">
                  <Icon name="local_police" className="absolute left-4 top-1/2 -translate-y-1/2 text-outline text-xl" />
                  <select
                    id="role"
                    value={roleId}
                    onChange={(e) => setRoleId(e.target.value)}
                    className="w-full pl-12 pr-4 py-3 bg-surface-container-low border border-outline-variant rounded-lg text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary-container transition-all appearance-none"
                  >
                    {SELF_REGISTRABLE_ROLES.map((r) => (
                      <option key={r.role_id} value={r.role_id}>
                        {r.role_name}
                      </option>
                    ))}
                  </select>
                </div>
                <p className="text-[11px] text-on-surface-variant px-1">
                  An administrator can adjust your role and station assignment when approving your account.
                </p>
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
                    placeholder="At least 8 characters"
                    required
                    minLength={8}
                    className="w-full pl-12 pr-4 py-3 bg-surface-container-low border border-outline-variant rounded-lg text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary-container transition-all"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-[11px] font-semibold tracking-wide uppercase text-on-surface-variant block" htmlFor="confirmPassword">
                  Confirm Password
                </label>
                <div className="relative">
                  <Icon name="lock" className="absolute left-4 top-1/2 -translate-y-1/2 text-outline text-xl" />
                  <input
                    id="confirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter password"
                    required
                    minLength={8}
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
                    Submitting...
                  </>
                ) : (
                  <>
                    Submit Registration
                    <Icon name="how_to_reg" className="text-lg" />
                  </>
                )}
              </button>

              <p className="text-center text-sm text-on-surface-variant">
                Already have an account?{" "}
                <Link to="/login" className="text-primary font-semibold hover:underline">
                  Log in
                </Link>
              </p>
            </form>
          )}
        </div>


      </main>
    </div>
  );
}
