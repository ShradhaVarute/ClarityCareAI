import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import apiClient from "../api/client";
import { useAuth } from "../context/AuthContext";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await apiClient.post("/auth/login", { email, password });
      login(response.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="min-h-screen grid md:grid-cols-2">
      {/* Brand panel */}
      <div className="hidden md:flex flex-col justify-between bg-deep text-paper p-12">
        <div>
          <p className="font-mono text-xs tracking-widest text-teal uppercase mb-2">
            Clarity Care AI
          </p>
          <h1 className="font-display text-4xl leading-tight max-w-sm">
            Explainable predictions, built for trust.
          </h1>
        </div>
        <p className="text-sm text-stone max-w-sm">
          Every result comes with the reasoning behind it — see exactly which
          factors shaped your assessment.
        </p>
      </div>

      {/* Form panel */}
      <div className="flex items-center justify-center p-8">
        <form onSubmit={handleSubmit} className="w-full max-w-sm">
          <h2 className="font-display text-2xl text-ink mb-1">Welcome back</h2>
          <p className="text-sm text-stone mb-6">Sign in to continue</p>

          {error && (
            <p className="text-coral text-sm mb-4 bg-coral/10 px-3 py-2 rounded">
              {error}
            </p>
          )}

          <label className="block text-xs font-medium text-stone uppercase tracking-wide mb-1">
            Email
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border border-stone/30 rounded-md px-3 py-2 mb-4 text-sm focus:outline-none focus:ring-2 focus:ring-teal"
            required
          />

          <label className="block text-xs font-medium text-stone uppercase tracking-wide mb-1">
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border border-stone/30 rounded-md px-3 py-2 mb-6 text-sm focus:outline-none focus:ring-2 focus:ring-teal"
            required
          />

          <button
            type="submit"
            className="w-full bg-deep text-paper rounded-md py-2.5 text-sm font-medium hover:bg-ink transition-colors"
          >
            Sign in
          </button>

          <p className="text-sm text-stone mt-5">
            No account?{" "}
            <Link to="/register" className="text-teal font-medium">
              Register
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}

export default Login;