import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import apiClient from "../api/client";
import DashboardLayout from "../components/DashboardLayout";
import ExplanationDisplay from "../components/ExplanationDisplay";

function DoctorPredictionDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    apiClient
      .get(`/doctor/predictions/${id}`)
      .then((res) => setDetail(res.data))
      .catch((err) => setError(err.response?.data?.detail || "Failed to load"));
  }, [id]);

  return (
    <DashboardLayout title="Assessment Detail">
      <button onClick={() => navigate(-1)} className="text-sm text-teal font-medium mb-6">
        ← Back
      </button>

      {error && <p className="text-coral text-sm">{error}</p>}

      {detail && (
        <>
          <div className="bg-white border border-stone/15 rounded-lg p-6 mb-6 max-w-3xl">
            <p className="text-xs font-medium text-stone uppercase tracking-wide mb-1">Patient</p>
            <p className="font-display text-xl text-ink mb-4">{detail.patient_name}</p>

            <p className="text-xs font-medium text-stone uppercase tracking-wide mb-1">Disease</p>
            <p className="font-display text-lg text-ink capitalize mb-4">
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

export default DoctorPredictionDetail;