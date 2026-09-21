import json

with open("feature_bounds_generated.json") as f:
    bounds = json.load(f)

# label, type, step per feature — carries the human-readable labels we already wrote,
# merged with real min/max pulled from the training data
METADATA = {
    "heart_disease": {
        "age": ("Age", "number", None), "sex": ("Sex (1 = male, 0 = female)", "number", None),
        "cp": ("Chest Pain Type", "number", None), "trestbps": ("Resting Blood Pressure", "number", None),
        "chol": ("Cholesterol", "number", None), "fbs": ("Fasting Blood Sugar > 120 (1/0)", "number", None),
        "restecg": ("Resting ECG (0-2)", "number", None), "thalach": ("Max Heart Rate Achieved", "number", None),
        "exang": ("Exercise Induced Angina (1/0)", "number", None), "oldpeak": ("ST Depression", "number", "0.1"),
        "slope": ("Slope of Peak Exercise ST", "number", None), "ca": ("Major Vessels Colored", "number", None),
        "thal": ("Thalassemia", "number", None),
    },
    "diabetes": {
        "pregnancies": ("Pregnancies", "number", None), "glucose": ("Glucose", "number", None),
        "blood_pressure": ("Blood Pressure", "number", None), "skin_thickness": ("Skin Thickness (mm)", "number", None),
        "insulin": ("Insulin", "number", None), "bmi": ("BMI", "number", "0.1"),
        "diabetes_pedigree": ("Diabetes Pedigree Function", "number", "0.01"), "age": ("Age", "number", None),
    },
    "kidney_disease": {
        "age": ("Age", "number", None), "bp": ("Blood Pressure", "number", None), "sg": ("Specific Gravity", "number", "0.001"),
        "al": ("Albumin", "number", None), "su": ("Sugar", "number", None), "bgr": ("Blood Glucose Random", "number", None),
        "bu": ("Blood Urea", "number", None), "sc": ("Serum Creatinine", "number", "0.1"), "sod": ("Sodium", "number", None),
        "pot": ("Potassium", "number", "0.1"), "hemo": ("Hemoglobin", "number", "0.1"), "pcv": ("Packed Cell Volume", "number", None),
        "wbcc": ("White Blood Cell Count", "number", None), "rbcc": ("Red Blood Cell Count", "number", "0.1"),
        "rbc_normal": ("RBC Normal? (1/0)", "number", None), "pc_normal": ("Pus Cell Normal? (1/0)", "number", None),
        "pcc_present": ("Pus Cell Clumps Present? (1/0)", "number", None), "ba_present": ("Bacteria Present? (1/0)", "number", None),
        "htn_yes": ("Hypertension? (1/0)", "number", None), "dm_no": ("Diabetes = No? (1/0)", "number", None),
        "dm_yes": ("Diabetes = Yes? (1/0)", "number", None), "cad_yes": ("Coronary Artery Disease? (1/0)", "number", None),
        "appet_poor": ("Poor Appetite? (1/0)", "number", None), "pe_yes": ("Pedal Edema? (1/0)", "number", None),
        "ane_yes": ("Anemia? (1/0)", "number", None),
    },
    "liver_disease": {
        "Age": ("Age", "number", None), "TB": ("Total Bilirubin", "number", "0.1"), "DB": ("Direct Bilirubin", "number", "0.1"),
        "Alkphos": ("Alkaline Phosphotase", "number", None), "Sgpt": ("Sgpt", "number", None), "Sgot": ("Sgot", "number", None),
        "TP": ("Total Proteins", "number", "0.1"), "ALB": ("Albumin", "number", "0.1"),
        "A/G Ratio": ("Albumin/Globulin Ratio", "number", "0.01"), "Gender_Male": ("Gender = Male? (1/0)", "number", None),
    },
    "stroke": {
        "age": ("Age", "number", None), "hypertension": ("Hypertension? (1/0)", "number", None),
        "heart_disease": ("Heart Disease? (1/0)", "number", None), "avg_glucose_level": ("Average Glucose Level", "number", "0.1"),
        "bmi": ("BMI", "number", "0.1"), "gender_Male": ("Gender = Male? (1/0)", "number", None),
        "gender_Other": ("Gender = Other? (1/0)", "number", None), "ever_married_Yes": ("Ever Married? (1/0)", "number", None),
        "work_type_Never_worked": ("Work Type = Never Worked? (1/0)", "number", None),
        "work_type_Private": ("Work Type = Private? (1/0)", "number", None),
        "work_type_Self-employed": ("Work Type = Self-Employed? (1/0)", "number", None),
        "work_type_children": ("Work Type = Child? (1/0)", "number", None),
        "Residence_type_Urban": ("Residence = Urban? (1/0)", "number", None),
        "smoking_status_formerly smoked": ("Formerly Smoked? (1/0)", "number", None),
        "smoking_status_never smoked": ("Never Smoked? (1/0)", "number", None),
        "smoking_status_smokes": ("Currently Smokes? (1/0)", "number", None),
    },
    "lung_cancer": {
        "AGE": ("Age", "number", None), "GENDER_Male": ("Gender = Male? (1/0)", "number", None),
        "SMOKING_YES": ("Smoking? (1/0)", "number", None), "YELLOW_FINGERS_YES": ("Yellow Fingers? (1/0)", "number", None),
        "ANXIETY_YES": ("Anxiety? (1/0)", "number", None), "PEER_PRESSURE_YES": ("Peer Pressure? (1/0)", "number", None),
        "CHRONIC DISEASE_YES": ("Chronic Disease? (1/0)", "number", None), "FATIGUE _YES": ("Fatigue? (1/0)", "number", None),
        "ALLERGY _YES": ("Allergy? (1/0)", "number", None), "WHEEZING_YES": ("Wheezing? (1/0)", "number", None),
        "ALCOHOL CONSUMING_YES": ("Alcohol Consuming? (1/0)", "number", None), "COUGHING_YES": ("Coughing? (1/0)", "number", None),
        "SHORTNESS OF BREATH_YES": ("Shortness of Breath? (1/0)", "number", None),
        "SWALLOWING DIFFICULTY_YES": ("Swallowing Difficulty? (1/0)", "number", None),
        "CHEST PAIN_YES": ("Chest Pain? (1/0)", "number", None),
    },
    "thyroid": {
        "age": ("Age", "number", None), "TSH": ("TSH Level", "number", "0.01"), "T3": ("T3 Level", "number", "0.1"),
        "TT4": ("TT4 Level", "number", None), "T4U": ("T4U Level", "number", "0.01"), "FTI": ("FTI Level", "number", None),
        "sex_M": ("Sex = Male? (1/0)", "number", None), "on_thyroxine_t": ("On Thyroxine? (1/0)", "number", None),
        "query_on_thyroxine_t": ("Query On Thyroxine? (1/0)", "number", None),
        "on_antithyroid_medication_t": ("On Antithyroid Medication? (1/0)", "number", None),
        "sick_t": ("Currently Sick? (1/0)", "number", None), "pregnant_t": ("Pregnant? (1/0)", "number", None),
        "thyroid_surgery_t": ("Had Thyroid Surgery? (1/0)", "number", None),
        "I131_treatment_t": ("I131 Treatment? (1/0)", "number", None),
        "query_hypothyroid_t": ("Query Hypothyroid? (1/0)", "number", None),
        "query_hyperthyroid_t": ("Query Hyperthyroid? (1/0)", "number", None), "lithium_t": ("On Lithium? (1/0)", "number", None),
        "goitre_t": ("Goitre? (1/0)", "number", None), "tumor_t": ("Tumor? (1/0)", "number", None),
        "hypopituitary_t": ("Hypopituitary? (1/0)", "number", None), "psych_t": ("Psychiatric Condition? (1/0)", "number", None),
        "referral_source_SVHC": ("Referral = SVHC? (1/0)", "number", None),
        "referral_source_SVHD": ("Referral = SVHD? (1/0)", "number", None),
        "referral_source_SVI": ("Referral = SVI? (1/0)", "number", None),
        "referral_source_other": ("Referral = Other? (1/0)", "number", None),
    },
    "hepatitis": {
        "Age": ("Age", "number", None), "Sex": ("Sex", "number", None), "Steroid": ("Steroid Use? (1/0)", "number", None),
        "Antivirals": ("Antivirals? (1/0)", "number", None), "Fatigue": ("Fatigue? (1/0)", "number", None),
        "Malaise": ("Malaise? (1/0)", "number", None), "Anorexia": ("Anorexia? (1/0)", "number", None),
        "Liver Big": ("Liver Enlarged? (1/0)", "number", None), "Liver Firm": ("Liver Firm? (1/0)", "number", None),
        "Spleen Palpable": ("Spleen Palpable? (1/0)", "number", None), "Spiders": ("Spider Angiomata? (1/0)", "number", None),
        "Ascites": ("Ascites? (1/0)", "number", None), "Varices": ("Varices? (1/0)", "number", None),
        "Bilirubin": ("Bilirubin", "number", "0.1"), "Alk Phosphate": ("Alk Phosphate", "number", None),
        "Sgot": ("Sgot", "number", None), "Albumin": ("Albumin", "number", "0.1"),
        "Protime": ("Prothrombin Time", "number", "0.1"), "Histology": ("Histology Result? (1/0)", "number", None),
    },
}

LABELS = {
    "heart_disease": "Heart Disease", "diabetes": "Diabetes", "breast_cancer": "Breast Cancer",
    "kidney_disease": "Kidney Disease", "liver_disease": "Liver Disease", "parkinsons": "Parkinson's Disease",
    "stroke": "Stroke", "lung_cancer": "Lung Cancer", "thyroid": "Thyroid Disease", "hepatitis": "Hepatitis",
}

lines = ["export const diseaseConfigs = {"]

for disease, features in bounds.items():
    lines.append(f'  {disease}: {{')
    lines.append(f'    label: "{LABELS[disease]}",')
    lines.append("    fields: [")
    for feat, (lo, hi) in features.items():
        if disease in ("breast_cancer", "parkinsons"):
            label = feat
            step = "0.001" if disease == "parkinsons" else "0.01"
        else:
            label, _, step = METADATA[disease][feat]
        step_str = f', step: "{step}"' if step else ""
        lines.append(f'      {{ name: {json.dumps(feat)}, label: {json.dumps(label)}, type: "number"{step_str}, min: {lo}, max: {hi} }},')
    lines.append("    ],")
    lines.append("  },")

lines.append("};")

with open("../frontend/src/config/diseaseConfigs.js", "w") as f:
    f.write("\n".join(lines) + "\n")

print("diseaseConfigs.js regenerated with real training-data bounds")