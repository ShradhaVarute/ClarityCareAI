import { useState, useEffect } from "react";
import apiClient from "../api/client";
import DashboardLayout from "../components/DashboardLayout";
import { diseaseConfigs } from "../config/diseaseConfigs";

function Insights() {
  const [disease, setDisease] = useState("heart_disease");
  const [data, setData] = useState([]);

  useEffect(() => {
    apiClient.get(`/predictions/insights/${disease}`).then((res) => setData(res.data));
  }, [disease]);

  const maxImportance = Math.max(...data.map((d) => d.importance), 0.001);

  return (
    <DashboardLayout title="Model Insights">
      <div className="bg-white border border-stone/15 rounded-lg p-6 max-w-2xl">
        <label className="block text-xs font-medium text-stone uppercase tracking-wide mb-2">Disease</label>
        <select
          value={disease}
          onChange={(e) => setDisease(e.target.value)}
          className="border border-stone/30 rounded-md px-3 py-2 mb-6 text-sm focus:outline-none focus:ring-2 focus:ring-teal"
        >
          {Object.entries(diseaseConfigs).map(([key, cfg]) => (
            <option key={key} value={key}>{cfg.label}</option>
          ))}
        </select>

        <h3 className="font-display text-lg text-ink mb-4">Most Influential Features</h3>
        <div className="space-y-3">
          {data.map((item) => (
            <div key={item.feature}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-ink">{item.feature}</span>
                <span className="font-mono text-xs text-stone">{item.importance.toFixed(3)}</span>
              </div>
              <div className="h-2 rounded-full bg-stone/15 overflow-hidden">
                <div
                  className="h-full bg-teal rounded-full"
                  style={{ width: `${(item.importance / maxImportance) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
}

export default Insights;