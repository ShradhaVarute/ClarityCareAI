import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import apiClient from "../api/client";
import DashboardLayout from "../components/DashboardLayout";
import ExplanationDisplay from "../components/ExplanationDisplay";

function PredictionDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    apiClient
      .get(`/predictions/history/${id}`)
      .then((res) => setDetail(res.data))
      .catch((err) => setError(err.response?.data?.detail || "Failed to load"));
  }, [id]);

  const handleDownload = async () => {
    const response = await apiClient.get(`/predictions/history/${id}/report`, { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `assessment_${id}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  return (
    <DashboardLayout title="Assessment Detail">
      <div className="flex items-center gap-4 mb-6">
        <button onClick={() => navigate("/dashboard")} className="text-sm text-teal font-medium">
          ← Back to Dashboard
        </button>
        {detail && (
          <button
            onClick={handleDownload}
            className="text-sm bg-deep text-paper px-4 py-2 rounded-md hover:bg-ink transition-colors"
          >
            Download PDF Report
          </button>
        )}
      </div>

      {error && <p className="text-coral text-sm">{error}</p>}

      {detail && (
        <>
          <div className="bg-white border border-stone/15 rounded-lg p-6 mb-6 max-w-3xl">
            <p className="text-xs font-medium text-stone uppercase tracking-wide mb-1">Disease</p>
            <p className="font-display text-xl text-ink capitalize mb-4">
              {detail.predicted_disease.replace("_", " ")}
            </p>
            <p className="text-xs font-medium text-stone uppercase tracking-wide mb-1">Date</p>
            <p className="font-mono text-sm text-ink mb-4">
              {new Date(detail.created_at).toLocaleString()}
            </p>
            <p className="text-xs font-medium text-stone uppercase tracking-wide mb-2">Input Values</p>
            <div className="grid grid-cols-2 gap-x-6 gap-y-1">
              {Object.entries(detail.input_features).map(([key, val]) => (
                <div key={key} className="flex justify-between text-sm border-b border-stone/10 py-1">
                  <span className="text-stone">{key}</span>
                  <span className="font-mono text-ink">{val}</span>
                </div>
              ))}
            </div>
          </div>

          <ExplanationDisplay
            result={{
              prediction: detail.prediction,
              confidence: Number(detail.confidence_score),
              explanation: detail.explanation,
            }}
            diseaseName={detail.predicted_disease}
          />
        </>
      )}
    </DashboardLayout>
  );
}

export default PredictionDetail;