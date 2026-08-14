import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import apiClient from "../api/client";
import DashboardLayout from "../components/DashboardLayout";
import PredictionForm from "../components/PredictionForm";
import ExplanationDisplay from "../components/ExplanationDisplay";
import { diseaseConfigs } from "../config/diseaseConfigs";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const { user } = useAuth();
  const [selectedDisease, setSelectedDisease] = useState("heart_disease");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const navigate = useNavigate();

  const loadHistory = () => {
    apiClient
      .get("/predictions/history")
      .then((res) => setHistory(res.data))
      .catch(() => {});
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handlePredict = async (features) => {
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const response = await apiClient.post(`/predictions/${selectedDisease}`, {
        patient_id: user?.patient_id,
        features,
      });
      setResult(response.data);
      loadHistory();
    } catch (err) {
      setError(err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const config = diseaseConfigs[selectedDisease];

  return (
    <DashboardLayout title="Patient Dashboard">
      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white border border-stone/15 rounded-lg p-6">
            <label className="block text-xs font-medium text-stone uppercase tracking-wide mb-2">
              Select Disease
            </label>
            <select
              value={selectedDisease}
              onChange={(e) => {
                setSelectedDisease(e.target.value);
                setResult(null);
              }}
              className="border border-stone/30 rounded-md px-3 py-2 mb-6 text-sm focus:outline-none focus:ring-2 focus:ring-teal"
            >
              {Object.entries(diseaseConfigs).map(([key, cfg]) => (
                <option key={key} value={key}>{cfg.label}</option>
              ))}
            </select>

            <PredictionForm key={selectedDisease} fields={config.fields} onSubmit={handlePredict} />

            {error && (
              <p className="text-coral text-sm mt-4 bg-coral/10 px-3 py-2 rounded">{error}</p>
            )}
            {loading && <p className="text-stone text-sm mt-4">Running prediction…</p>}
          </div>

          {result && <ExplanationDisplay result={result} diseaseName={selectedDisease} />}
        </div>

        <div className="bg-white border border-stone/15 rounded-lg p-6 h-fit">
          <h3 className="font-display text-lg text-ink mb-4">Recent Assessments</h3>
          {history.length === 0 && (
            <p className="text-sm text-stone">No assessments yet.</p>
          )}
          <ul className="space-y-3">
            {history.slice(0, 8).map((h) => (
              <li
              key={h.id}
              onClick={() => navigate(`/predictions/${h.id}`)}
              className="border-b border-stone/10 pb-3 cursor-pointer hover:bg-paper/60 -mx-2 px-2 rounded transition-colors"
            >
              <p className="text-sm text-ink capitalize">{h.predicted_disease.replace("_", " ")}</p>
              <div className="flex justify-between items-center mt-1">
                <span className="font-mono text-xs text-stone">
                  {new Date(h.created_at).toLocaleDateString()}
                </span>
                <span className="font-mono text-xs text-teal">
                  {(Number(h.confidence_score) * 100).toFixed(0)}%
                </span>
              </div>
            </li>
            ))}
          </ul>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default Dashboard;