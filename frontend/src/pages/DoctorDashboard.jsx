import { useState, useEffect } from "react";
import apiClient from "../api/client";
import DashboardLayout from "../components/DashboardLayout";
import { useNavigate } from "react-router-dom";

function DoctorDashboard() {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

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

  return (
    <DashboardLayout title="Doctor Dashboard">
      {error && <p className="text-coral text-sm mb-4 bg-coral/10 px-3 py-2 rounded">{error}</p>}

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="bg-white border border-stone/15 rounded-lg p-6">
          <h2 className="font-display text-lg text-ink mb-4">Patients</h2>
          <ul className="space-y-1">
            {patients.map((p) => (
              <li key={p.id}>
                <button
                  onClick={() => handleSelectPatient(p)}
                  className={`w-full text-left px-3 py-2.5 rounded-md text-sm transition-colors ${selectedPatient?.id === p.id
                      ? "bg-deep text-paper"
                      : "text-ink hover:bg-paper"
                    }`}
                >
                  {p.full_name}
                </button>
              </li>
            ))}
            {patients.length === 0 && (
              <p className="text-sm text-stone">No patients yet.</p>
            )}
          </ul>
        </div>

        <div className="lg:col-span-2 bg-white border border-stone/15 rounded-lg p-6">
          <h2 className="font-display text-lg text-ink mb-4">
            {selectedPatient ? `${selectedPatient.full_name}'s History` : "Select a patient"}
          </h2>

          {!selectedPatient && (
            <p className="text-sm text-stone">Choose a patient from the list to view their assessment history.</p>
          )}

          <div className="space-y-3">
            {history.map((pred) => (
              <div
                key={pred.id}
                onClick={() => navigate(`/doctor/predictions/${pred.id}`)}
                className="border border-stone/10 rounded-md p-4 cursor-pointer hover:bg-paper transition-colors"
              >
                <div className="flex justify-between items-center mb-1">
                  <p className="text-sm text-ink capitalize">{pred.predicted_disease.replace("_", " ")}</p>
                  <span className="font-mono text-xs text-teal">
                    {(Number(pred.confidence_score) * 100).toFixed(0)}%
                  </span>
                </div>
                <p className="font-mono text-xs text-stone">
                  {new Date(pred.created_at).toLocaleString()}
                </p>
              </div>
            ))}
            {selectedPatient && history.length === 0 && (
              <p className="text-sm text-stone">No predictions yet for this patient.</p>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default DoctorDashboard;