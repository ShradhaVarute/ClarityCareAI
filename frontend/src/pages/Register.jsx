import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import apiClient from "../api/client";
import { useAuth } from "../context/AuthContext";

function Register() {
  const [formData, setFormData] = useState({
    email: "", password: "", full_name: "", role: "patient",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await apiClient.post("/auth/register", formData);
      login(response.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  const inputClass = "w-full border border-stone/30 rounded-md px-3 py-2 mb-4 text-sm focus:outline-none focus:ring-2 focus:ring-teal";
  const labelClass = "block text-xs font-medium text-stone uppercase tracking-wide mb-1";

  return (
    <div className="min-h-screen grid md:grid-cols-2">
      <div className="hidden md:flex flex-col justify-between bg-deep text-paper p-12">
        <div>
          <p className="font-mono text-xs tracking-widest text-teal uppercase mb-2">Clarity Care AI</p>
          <h1 className="font-display text-4xl leading-tight max-w-sm">
            Ten conditions. One clear answer, every time.
          </h1>
        </div>
        <p className="text-sm text-stone max-w-sm">
          Register as a patient to run assessments, or as a doctor to review patient history.
        </p>
      </div>

      <div className="flex items-center justify-center p-8">
        <form onSubmit={handleSubmit} className="w-full max-w-sm">
          <h2 className="font-display text-2xl text-ink mb-1">Create an account</h2>
          <p className="text-sm text-stone mb-6">Get started with Clarity Care AI</p>

          {error && (
            <p className="text-coral text-sm mb-4 bg-coral/10 px-3 py-2 rounded">{error}</p>
          )}

          <label className={labelClass}>Full Name</label>
          <input name="full_name" value={formData.full_name} onChange={handleChange} className={inputClass} required />

          <label className={labelClass}>Email</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} className={inputClass} required />

          <label className={labelClass}>Password</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} className={inputClass} required />

          <label className={labelClass}>Role</label>
          <select name="role" value={formData.role} onChange={handleChange} className={inputClass}>
            <option value="patient">Patient</option>
            <option value="doctor">Doctor</option>
          </select>

          <button type="submit" className="w-full bg-deep text-paper rounded-md py-2.5 text-sm font-medium hover:bg-ink transition-colors mt-2">
            Create account
          </button>

          <p className="text-sm text-stone mt-5">
            Already have an account? <Link to="/login" className="text-teal font-medium">Login</Link>
          </p>
        </form>
      </div>
    </div>
  );
}

export default Register;