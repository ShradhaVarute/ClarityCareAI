import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client";

function AdminDashboard() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([apiClient.get("/admin/stats"), apiClient.get("/admin/users")])
      .then(([statsRes, usersRes]) => {
        setStats(statsRes.data);
        setUsers(usersRes.data);
      })
      .catch((err) => setError(err.response?.data?.detail || "Failed to load admin data"));
  }, []);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-slate-100 p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Admin Dashboard</h1>
        <button onClick={handleLogout} className="bg-red-600 text-white px-4 py-2 rounded">
          Logout
        </button>
      </div>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      {stats && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg shadow-md">
            <p className="text-slate-500 text-sm">Total Users</p>
            <p className="text-2xl font-bold text-slate-800">{stats.total_users}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <p className="text-slate-500 text-sm">Patients</p>
            <p className="text-2xl font-bold text-slate-800">{stats.total_patients}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <p className="text-slate-500 text-sm">Doctors</p>
            <p className="text-2xl font-bold text-slate-800">{stats.total_doctors}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <p className="text-slate-500 text-sm">Total Predictions</p>
            <p className="text-2xl font-bold text-slate-800">{stats.total_predictions}</p>
          </div>
        </div>
      )}

      {stats && (
        <div className="bg-white p-4 rounded-lg shadow-md mb-6">
          <h2 className="font-semibold text-slate-800 mb-3">Predictions by Disease</h2>
          <ul className="grid grid-cols-2 gap-2 text-sm">
            {Object.entries(stats.predictions_by_disease).map(([disease, count]) => (
              <li key={disease} className="flex justify-between border-b pb-1">
                <span className="text-slate-700">{disease}</span>
                <span className="text-slate-500">{count}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="bg-white p-4 rounded-lg shadow-md">
        <h2 className="font-semibold text-slate-800 mb-3">All Users</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-500 border-b">
              <th className="pb-2">Email</th>
              <th className="pb-2">Role</th>
              <th className="pb-2">Joined</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-b">
                <td className="py-2">{u.email}</td>
                <td className="py-2 capitalize">{u.role}</td>
                <td className="py-2">{new Date(u.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AdminDashboard;