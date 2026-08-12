import { useState } from "react";

function PredictionForm({ fields, onSubmit }) {
  const [values, setValues] = useState(
    Object.fromEntries(fields.map((f) => [f.name, ""]))
  );

  const handleChange = (name, value) => {
    setValues({ ...values, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
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
            value={values[field.name]}
            onChange={(e) => handleChange(field.name, e.target.value)}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
      ))}
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