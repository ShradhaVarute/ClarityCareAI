import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client";
import PredictionForm from "../components/PredictionForm";
import ExplanationDisplay from "../components/ExplanationDisplay";
import { diseaseConfigs } from "../config/diseaseConfigs";

function Dashboard() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const [selectedDisease, setSelectedDisease] = useState("heart_disease");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const handlePredict = async (features) => {
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const response = await apiClient.post(`/predictions/${selectedDisease}`, {
        patient_id: user?.patient_id, // TEMPORARY — hardcoded for now, real patient linkage in next step
        features,
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const config = diseaseConfigs[selectedDisease];

  return (
    <div className="min-h-screen bg-slate-100 p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Patient Dashboard</h1>
        <button onClick={handleLogout} className="bg-red-600 text-white px-4 py-2 rounded">
          Logout
        </button>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md max-w-3xl">
        <label className="block text-sm text-slate-600 mb-2">Select Disease</label>
        <select
          value={selectedDisease}
          onChange={(e) => {
            setSelectedDisease(e.target.value);
            setResult(null);
          }}
          className="border rounded px-3 py-2 mb-6"
        >
          {Object.entries(diseaseConfigs).map(([key, cfg]) => (
            <option key={key} value={key}>{cfg.label}</option>
          ))}
        </select>

        <PredictionForm key={selectedDisease} fields={config.fields} onSubmit={handlePredict} />

        {error && <p className="text-red-600 mt-4">{error}</p>}
        {loading && <p className="text-slate-500 mt-4">Running prediction...</p>}
      </div>

      {result && <ExplanationDisplay result={result} />}
    </div>
  );
}

export default Dashboard;