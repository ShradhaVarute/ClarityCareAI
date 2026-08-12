function ExplanationDisplay({ result }) {
  const { prediction, confidence, explanation } = result;
  const topFactors = explanation.slice(0, 5);

  return (
    <div className="mt-6 bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-lg font-bold text-slate-800 mb-2">Result</h2>
      <p className="text-slate-700 mb-1">
        Prediction:{" "}
        <span className={prediction === 1 ? "text-red-600 font-semibold" : "text-green-600 font-semibold"}>
          {prediction === 1 ? "Condition Likely Present" : "Condition Unlikely"}
        </span>
      </p>
      <p className="text-slate-600 mb-4">
        Confidence: {(confidence * 100).toFixed(1)}%
      </p>

      <h3 className="font-semibold text-slate-800 mb-2">Top Contributing Factors</h3>
      <ul className="space-y-2">
        {topFactors.map((item) => (
          <li key={item.feature} className="flex justify-between text-sm border-b pb-1">
            <span className="text-slate-700">
              {item.feature} = {item.input_value}
            </span>
            <span className={item.shap_value > 0 ? "text-red-600" : "text-green-600"}>
              {item.shap_value > 0 ? "↑ increases risk" : "↓ decreases risk"} ({item.shap_value.toFixed(3)})
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ExplanationDisplay;