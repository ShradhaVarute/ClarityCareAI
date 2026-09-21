import { useState, useEffect } from "react";

function PredictionForm({ fields, onSubmit }) {
  const [values, setValues] = useState(
    Object.fromEntries(fields.map((f) => [f.name, ""]))
  );
  const [error, setError] = useState("");

  useEffect(() => {
    setValues(Object.fromEntries(fields.map((f) => [f.name, ""])));
    setError("");
  }, [fields]);

  const handleChange = (name, value) => {
    setValues({ ...values, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    for (const field of fields) {
      const raw = values[field.name];
      const num = Number(raw);

      if (raw === "" || Number.isNaN(num)) {
        setError(`${field.label} must be a valid number.`);
        return;
      }
      if (field.min !== undefined && num < field.min) {
        setError(`${field.label} must be at least ${field.min}.`);
        return;
      }
      if (field.max !== undefined && num > field.max) {
        setError(`${field.label} must be no more than ${field.max}.`);
        return;
      }
    }

    const numericValues = Object.fromEntries(
      Object.entries(values).map(([k, v]) => [k, Number(v)])
    );
    onSubmit(numericValues);
  };

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
      {fields.map((field) => (
        <div key={field.name}>
          <label className="block text-sm text-slate-600 mb-1">{field.label}</label>
          <input
            type={field.type}
            step={field.step || "1"}
            min={field.min}
            max={field.max}
            value={values[field.name]}
            onChange={(e) => handleChange(field.name, e.target.value)}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
      ))}
      {error && (
        <p className="col-span-2 text-coral text-sm bg-coral/10 px-3 py-2 rounded">
          {error}
        </p>
      )}
      <button
        type="submit"
        className="col-span-2 bg-slate-800 text-white rounded py-2 mt-2"
      >
        Predict
      </button>
    </form>
  );
}

export default PredictionForm;