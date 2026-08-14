function ConfidenceGauge({ confidence, prediction }) {
    const pct = confidence * 100;
    const zoneColor = prediction === 1 ? "bg-coral" : "bg-teal";
  
    return (
      <div className="mt-1">
        <div className="flex justify-between items-baseline mb-2">
          <span className="text-xs font-medium text-stone uppercase tracking-wide">Confidence</span>
          <span className="font-mono text-lg text-ink">{pct.toFixed(1)}%</span>
        </div>
  
        <div className="relative h-3 rounded-full bg-stone/15 overflow-hidden">
          <div
            className={`absolute inset-y-0 left-0 rounded-full ${zoneColor} transition-all duration-500`}
            style={{ width: `${pct}%` }}
          />
        </div>
  
        <div className="flex justify-between mt-1">
          <span className="font-mono text-[10px] text-stone">0</span>
          <span className="font-mono text-[10px] text-stone">50</span>
          <span className="font-mono text-[10px] text-stone">100</span>
        </div>
      </div>
    );
  }
  
  export default ConfidenceGauge;