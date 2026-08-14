import ConfidenceGauge from "./ConfidenceGauge";
import RiskSuggestions from "./RiskSuggestions";

function ExplanationDisplay({ result, diseaseName }) {
  const { prediction, confidence, explanation } = result;
  const topFactors = explanation.slice(0, 5);

  return (
    <>
      <div className="mt-6 bg-white border border-stone/15 rounded-lg p-6 max-w-3xl">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-display text-xl text-ink">Assessment</h2>
          <span
            className={`text-xs font-mono uppercase tracking-wide px-2.5 py-1 rounded-full ${
              prediction === 1 ? "bg-coral/10 text-coral" : "bg-teal/10 text-teal"
            }`}
          >
            {prediction === 1 ? "Condition Likely Present" : "Condition Unlikely"}
          </span>
        </div>

        <ConfidenceGauge confidence={confidence} prediction={prediction} />

        <h3 className="font-display text-sm text-ink mt-6 mb-3">Top Contributing Factors</h3>
        <ul className="space-y-1">
          {topFactors.map((item) => (
            <li key={item.feature} className="flex justify-between items-center text-sm border-b border-stone/10 py-2">
              <span className="text-ink">
                {item.feature} <span className="font-mono text-stone">= {item.input_value}</span>
              </span>
              <span className={`font-mono text-xs ${item.shap_value > 0 ? "text-coral" : "text-teal"}`}>
                {item.shap_value > 0 ? "↑" : "↓"} {item.shap_value.toFixed(3)}
              </span>
            </li>
          ))}
        </ul>
      </div>
      {prediction === 1 && diseaseName && (
        <RiskSuggestions explanation={explanation} diseaseName={diseaseName} />
      )}
    </>
  );
}

export default ExplanationDisplay;