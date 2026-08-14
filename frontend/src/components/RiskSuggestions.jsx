import { getSuggestions } from "../utils/riskSuggestions";

function RiskSuggestions({ explanation, diseaseName }) {
  const suggestions = getSuggestions(explanation, diseaseName);

  if (suggestions.length === 0) return null;

  return (
    <div className="mt-6 bg-teal/5 border border-teal/20 rounded-lg p-6 max-w-3xl">
      <h3 className="font-display text-sm text-ink mb-3">Lifestyle Factors to Discuss</h3>
      <ul className="space-y-2 mb-4">
        {suggestions.map((s) => (
          <li key={s.feature} className="text-sm text-ink flex gap-2">
            <span className="text-teal">•</span>
            <span>{s.text}</span>
          </li>
        ))}
      </ul>
      <p className="text-xs text-stone italic border-t border-teal/20 pt-3">
        These are general informational points, not medical advice. Please consult a
        qualified healthcare professional before making any health decisions.
      </p>
    </div>
  );
}

export default RiskSuggestions;