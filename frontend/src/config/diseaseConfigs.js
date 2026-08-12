export const diseaseConfigs = {
    heart_disease: {
      label: "Heart Disease",
      fields: [
        { name: "age", label: "Age", type: "number" },
        { name: "sex", label: "Sex (1 = male, 0 = female)", type: "number" },
        { name: "cp", label: "Chest Pain Type (0-3)", type: "number" },
        { name: "trestbps", label: "Resting Blood Pressure", type: "number" },
        { name: "chol", label: "Cholesterol", type: "number" },
        { name: "fbs", label: "Fasting Blood Sugar > 120 (1/0)", type: "number" },
        { name: "restecg", label: "Resting ECG (0-2)", type: "number" },
        { name: "thalach", label: "Max Heart Rate Achieved", type: "number" },
        { name: "exang", label: "Exercise Induced Angina (1/0)", type: "number" },
        { name: "oldpeak", label: "ST Depression", type: "number", step: "0.1" },
        { name: "slope", label: "Slope of Peak Exercise ST (0-2)", type: "number" },
        { name: "ca", label: "Major Vessels Colored (0-3)", type: "number" },
        { name: "thal", label: "Thalassemia (1-3)", type: "number" },
      ],
    },
    diabetes: {
      label: "Diabetes",
      fields: [
        { name: "pregnancies", label: "Pregnancies", type: "number" },
        { name: "glucose", label: "Glucose", type: "number" },
        { name: "blood_pressure", label: "Blood Pressure", type: "number" },
        { name: "skin_thickness", label: "Skin Thickness", type: "number" },
        { name: "insulin", label: "Insulin", type: "number" },
        { name: "bmi", label: "BMI", type: "number", step: "0.1" },
        { name: "diabetes_pedigree", label: "Diabetes Pedigree Function", type: "number", step: "0.01" },
        { name: "age", label: "Age", type: "number" },
      ],
    },
  };