import { useState, useContext } from "react";
import { useNavigate, Link, useLocation } from "react-router-dom";
import { Shield, Loader2, Eye, EyeOff, ArrowLeft, UserPlus, LogIn } from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { AuthContext } from "../App";
import { authAPI } from "../services/api";
import { toast } from "sonner";

export default function AdminLogin({ adminOnly = false }) {
  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();
  const returnTo = location.state?.from || "/";
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("login");

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) {
      toast.error("Email and password are required");
      return;
    }
    try {
      setLoading(true);
      const res =
        mode === "register" && !adminOnly
          ? await authAPI.register({
              email,
              username,
              password,
              password_confirm: passwordConfirm,
            })
          : await authAPI.login({ email, password });
      const data = res.data.data;
      const role = data.user?.role;
      if (adminOnly && role !== "admin" && role !== "super_admin") {
        toast.error("This account does not have admin access.");
        return;
      }
      localStorage.setItem("accessToken", data.tokens.access);
      localStorage.setItem("refreshToken", data.tokens.refresh);
      setUser(data.user);
      toast.success(adminOnly ? "Welcome back, admin!" : "Welcome to CodeCache!");
      navigate(adminOnly ? "/admin" : returnTo, { replace: true });
    } catch (error) {
      const msg =
        error.response?.data?.error?.message ||
        "Login failed. Check credentials.";
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 flex items-center justify-center">
      <div className="w-full max-w-md">
        <Link
          to={returnTo}
          className="inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-primary transition-colors mb-6"
        >
          <ArrowLeft className="h-3.5 w-3.5" /> Back to Home
        </Link>

        <div
          className="bg-card rounded-xl p-6 md:p-8"
          style={{
            border: "2px solid var(--line)",
            boxShadow: "var(--shadow-primary)",
          }}
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <Shield className="h-5 w-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-bold">
                {adminOnly ? "Admin Login" : mode === "register" ? "Create Account" : "Login"}
              </h1>
              <p className="text-sm text-ink-soft">
                {adminOnly
                  ? "Access the CodeCache control panel"
                  : "Track progress, save snippets, and keep your learning path"}
              </p>
            </div>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            {!adminOnly && (
              <div className="grid grid-cols-2 gap-2 rounded-lg bg-muted p-1">
                <button
                  type="button"
                  onClick={() => setMode("login")}
                  className={`rounded-md px-3 py-2 text-sm font-bold ${mode === "login" ? "bg-card" : ""}`}
                >
                  Login
                </button>
                <button
                  type="button"
                  onClick={() => setMode("register")}
                  className={`rounded-md px-3 py-2 text-sm font-bold ${mode === "register" ? "bg-card" : ""}`}
                >
                  Register
                </button>
              </div>
            )}
            {mode === "register" && !adminOnly ? (
              <div>
                <label className="text-xs font-medium text-ink-soft block mb-1">
                  Username
                </label>
                <Input
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="yourname"
                  autoComplete="username"
                />
              </div>
            ) : null}
            <div>
              <label className="text-xs font-medium text-ink-soft block mb-1">
                Email
              </label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@codecache.com"
                autoFocus
                autoComplete="email"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-ink-soft block mb-1">
                Password
              </label>
              <div className="relative">
                <Input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  autoComplete="current-password"
                  className="pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-soft hover:text-foreground"
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>
            {mode === "register" && !adminOnly ? (
              <div>
                <label className="text-xs font-medium text-ink-soft block mb-1">
                  Confirm Password
                </label>
                <Input
                  type={showPassword ? "text" : "password"}
                  value={passwordConfirm}
                  onChange={(e) => setPasswordConfirm(e.target.value)}
                  placeholder="••••••••"
                  autoComplete="new-password"
                />
              </div>
            ) : null}
            <Button type="submit" className="w-full gap-2" disabled={loading}>
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : mode === "register" && !adminOnly ? (
                <UserPlus className="h-4 w-4" />
              ) : (
                <LogIn className="h-4 w-4" />
              )}
              {loading ? "Signing in..." : mode === "register" && !adminOnly ? "Create Account" : "Sign In"}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
