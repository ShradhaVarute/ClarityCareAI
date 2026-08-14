import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { Link, useLocation } from "react-router-dom";

function DashboardLayout({ title, children }) {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex">
      <aside className="w-56 bg-deep text-paper flex flex-col justify-between p-6">
        <div>
          <p className="font-mono text-xs tracking-widest text-teal uppercase mb-8">
            Clarity Care AI
          </p>
          <nav className="space-y-1">
            <Link
              to="/dashboard"
              className={`block text-sm rounded-md px-3 py-2 transition-colors ${location.pathname === "/dashboard" ? "bg-white/10 text-paper" : "text-stone hover:bg-white/5"
                }`}
            >
              Overview
            </Link>
            <Link
              to="/insights"
              className={`block text-sm rounded-md px-3 py-2 transition-colors ${location.pathname === "/insights" ? "bg-white/10 text-paper" : "text-stone hover:bg-white/5"
                }`}
            >
              Model Insights
            </Link>
          </nav>
        </div>
        <div>
          <p className="text-xs text-stone mb-3 truncate">{user?.email}</p>
          <button
            onClick={handleLogout}
            className="w-full text-left text-sm text-coral hover:text-paper transition-colors"
          >
            Logout →
          </button>
        </div>
      </aside>

      <main className="flex-1 bg-paper p-10">
        <h1 className="font-display text-3xl text-ink mb-8">{title}</h1>
        {children}
      </main>
    </div>
  );
}

export default DashboardLayout;