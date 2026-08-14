import { useState, useEffect } from "react";
import apiClient from "../api/client";
import DashboardLayout from "../components/DashboardLayout";

function StatCard({ label, value }) {
  return (
    <div className="bg-white border border-stone/15 rounded-lg p-5">
      <p className="text-xs font-medium text-stone uppercase tracking-wide mb-1">{label}</p>
      <p className="font-display text-3xl text-ink">{value}</p>
    </div>
  );
}

function AdminDashboard() {
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

  return (
    <DashboardLayout title="Admin Dashboard">
      {error && <p className="text-coral text-sm mb-4 bg-coral/10 px-3 py-2 rounded">{error}</p>}

      {stats && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <StatCard label="Total Users" value={stats.total_users} />
            <StatCard label="Patients" value={stats.total_patients} />
            <StatCard label="Doctors" value={stats.total_doctors} />
            <StatCard label="Predictions" value={stats.total_predictions} />
          </div>

          <div className="bg-white border border-stone/15 rounded-lg p-6 mb-6">
            <h2 className="font-display text-lg text-ink mb-4">Predictions by Disease</h2>
            <ul className="grid grid-cols-2 gap-x-8 gap-y-1">
              {Object.entries(stats.predictions_by_disease).map(([disease, count]) => (
                <li key={disease} className="flex justify-between text-sm border-b border-stone/10 py-2">
                  <span className="text-ink capitalize">{disease.replace("_", " ")}</span>
                  <span className="font-mono text-teal">{count}</span>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}

      <div className="bg-white border border-stone/15 rounded-lg p-6">
        <h2 className="font-display text-lg text-ink mb-4">All Users</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs text-stone uppercase tracking-wide border-b border-stone/15">
              <th className="pb-3 font-medium">Email</th>
              <th className="pb-3 font-medium">Role</th>
              <th className="pb-3 font-medium">Joined</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-b border-stone/10">
                <td className="py-3 text-ink">{u.email}</td>
                <td className="py-3">
                  <span className="text-xs font-mono uppercase text-stone">{u.role}</span>
                </td>
                <td className="py-3 font-mono text-xs text-stone">
                  {new Date(u.created_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardLayout>
  );
}

export default AdminDashboard;