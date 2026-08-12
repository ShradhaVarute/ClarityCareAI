import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client";

function DoctorDashboard() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    apiClient
      .get("/doctor/patients")
      .then((res) => setPatients(res.data))
      .catch((err) => setError(err.response?.data?.detail || "Failed to load patients"));
  }, []);

  const handleSelectPatient = async (patient) => {
    setSelectedPatient(patient);
    setError("");
    try {
      const res = await apiClient.get(`/doctor/patients/${patient.id}/predictions`);
      setHistory(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load history");
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-slate-100 p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Doctor Dashboard</h1>
        <button onClick={handleLogout} className="bg-red-600 text-white px-4 py-2 rounded">
          Logout
        </button>
      </div>

      {error && <p className="text-red-600 mb-4">{error}</p>}

      <div className="grid grid-cols-3 gap-6">
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h2 className="font-semibold text-slate-800 mb-3">Patients</h2>
          <ul className="space-y-2">
            {patients.map((p) => (
              <li key={p.id}>
                <button
                  onClick={() => handleSelectPatient(p)}
                  className={`w-full text-left px-3 py-2 rounded ${
                    selectedPatient?.id === p.id ? "bg-slate-800 text-white" : "bg-slate-100"
                  }`}
                >
                  {p.full_name}
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="col-span-2 bg-white p-4 rounded-lg shadow-md">
          <h2 className="font-semibold text-slate-800 mb-3">
            {selectedPatient ? `${selectedPatient.full_name}'s History` : "Select a patient"}
          </h2>
          <div className="space-y-3">
            {history.map((pred) => (
              <div key={pred.id} className="border rounded p-3">
                <p className="font-medium text-slate-800">
                  {pred.predicted_disease} — confidence {(Number(pred.confidence_score) * 100).toFixed(1)}%
                </p>
                <p className="text-xs text-slate-500">{new Date(pred.created_at).toLocaleString()}</p>
              </div>
            ))}
            {selectedPatient && history.length === 0 && (
              <p className="text-slate-500 text-sm">No predictions yet for this patient.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DoctorDashboard;