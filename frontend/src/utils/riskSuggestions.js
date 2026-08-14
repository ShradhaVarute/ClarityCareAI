// Per-disease, curated lifestyle pointers for modifiable risk factors.
// Explicitly NOT medical advice — always paired with a disclaimer in the UI.
// Diseases with no genuinely modifiable factors (e.g. tumor biopsy measurements,
// voice biomarkers) intentionally have no rules and will show nothing.

const DISEASE_RULES = {
  heart_disease: [
    { match: /^chol$/i, text: "Cholesterol is often improved through diet (less saturated fat) and regular exercise." },
    { match: /^trestbps$/i, text: "Resting blood pressure can often be managed through diet, exercise, and reduced sodium intake." },
    { match: /^fbs$/i, text: "Fasting blood sugar above normal levels can be improved through diet and physical activity." },
    { match: /^exang$/i, text: "Exercise-induced symptoms are worth discussing with a doctor before starting any new activity plan." },
    { match: /^thalach$/i, text: "Cardiovascular fitness (reflected in heart rate response) can improve with regular moderate exercise." },
  ],

  diabetes: [
    { match: /^glucose$/i, text: "Blood glucose levels can often be improved through diet, weight management, and physical activity." },
    { match: /^bmi$/i, text: "BMI is a modifiable factor through a balanced diet and regular physical activity." },
    { match: /^insulin$/i, text: "Insulin response can be influenced by diet, weight, and activity level — worth discussing with a doctor." },
    { match: /^blood_pressure$/i, text: "Blood pressure can often be managed through diet, exercise, and reduced sodium intake." },
  ],

  breast_cancer: [], // Features are biopsy/imaging measurements — nothing lifestyle-modifiable to suggest

  kidney_disease: [
    { match: /^bu$/i, text: "Elevated blood urea can be influenced by hydration and protein intake — best discussed with a doctor." },
    { match: /^htn_yes$/i, text: "Managing blood pressure through diet, exercise, and reduced sodium can help protect kidney function." },
    { match: /^dm_yes$/i, text: "Managing blood sugar levels helps reduce further strain on kidney function." },
    { match: /^appet_poor$/i, text: "Poor appetite affecting nutrition is worth raising with a doctor or dietitian." },
    { match: /^pe_yes$/i, text: "Swelling (edema) can sometimes be eased with reduced salt intake — consult a doctor." },
  ],

  liver_disease: [
    { match: /^tb$|^db$/i, text: "Elevated bilirubin is often linked to liver strain — reducing alcohol intake can help." },
    { match: /^sgpt$|^sgot$/i, text: "Elevated liver enzymes are commonly improved by reducing alcohol and maintaining a balanced diet." },
    { match: /^alkphos$/i, text: "Alkaline phosphatase levels can be influenced by diet and liver health — worth discussing with a doctor." },
  ],

  parkinsons: [], // Voice-measurement biomarkers — no lifestyle-modifiable equivalent

  stroke: [
    { match: /^hypertension$/i, text: "Managing blood pressure through diet, exercise, and reduced sodium is one of the most effective ways to lower stroke risk." },
    { match: /^avg_glucose_level$/i, text: "Blood glucose levels can often be improved through diet and physical activity." },
    { match: /^bmi$/i, text: "BMI is a modifiable factor through a balanced diet and regular physical activity." },
    { match: /^smoking_status_smokes$/i, text: "Smoking cessation is one of the most impactful changes for reducing stroke risk." },
    { match: /^smoking_status_formerly smoked$/i, text: "Continuing to avoid smoking helps sustain lowered risk over time." },
  ],

  lung_cancer: [
    { match: /^smoking_yes$/i, text: "Smoking cessation is the single most impactful change for reducing lung cancer risk." },
    { match: /^alcohol consuming_yes$/i, text: "Reducing alcohol intake can support overall respiratory and general health." },
    { match: /^coughing_yes$|^wheezing_yes$|^shortness of breath_yes$/i, text: "Persistent respiratory symptoms are worth discussing with a doctor promptly." },
    { match: /^peer_pressure_yes$/i, text: "Avoiding smoking-related peer environments can help reduce ongoing exposure." },
  ],

  thyroid: [
    { match: /^sick_t$/i, text: "Ongoing illness affecting thyroid readings is worth discussing with a doctor for proper management." },
    { match: /^psych_t$/i, text: "Psychiatric symptoms alongside thyroid changes are worth raising with a doctor, as the two can be related." },
  ],

  hepatitis: [
    { match: /^antivirals$/i, text: "Following prescribed antiviral treatment as directed by a doctor is important for management." },
    { match: /^alk phosphate$|^sgot$/i, text: "Elevated liver enzymes are commonly improved by reducing alcohol and maintaining a balanced diet." },
    { match: /^albumin$/i, text: "Low albumin can be linked to nutrition — a balanced, protein-appropriate diet may help, under medical guidance." },
    { match: /^fatigue$|^malaise$|^anorexia$/i, text: "Persistent fatigue or appetite loss should be discussed with a doctor, as they can have several causes." },
  ],
};

// Factors that should never be suggested as "modifiable" even if a rule matches by accident
const NON_MODIFIABLE = /^age$|^sex$|^gender|^AGE$|thal$|referral_source|histology/i;

export function getSuggestions(explanation, diseaseName) {
  const rules = DISEASE_RULES[diseaseName] || [];
  if (rules.length === 0) return [];

  const riskFactors = explanation.filter((item) => item.shap_value > 0);
  const suggestions = [];
  const seen = new Set();

  for (const factor of riskFactors) {
    if (NON_MODIFIABLE.test(factor.feature)) continue;

    const rule = rules.find((r) => r.match.test(factor.feature));
    if (rule && !seen.has(rule.text)) {
      suggestions.push({ feature: factor.feature, text: rule.text });
      seen.add(rule.text);
    }
  }

  return suggestions.slice(0, 4);
}