# Clarity Care AI

**Explainable Disease Prediction Using Machine Learning** — a final year CS engineering major project.

🔗 **Live app**: https://clarity-care-ai-hbru.vercel.app
🔗 **API docs**: https://claritycareai.onrender.com/docs

> Note: the backend runs on a free-tier host and may take 30–60 seconds to respond on first load after inactivity.

## What it does

Clarity Care AI predicts risk across **10 diseases** — Heart Disease, Diabetes, Breast Cancer, Chronic Kidney Disease, Liver Disease, Parkinson's, Stroke, Lung Cancer, Thyroid Disease, and Hepatitis — and explains every prediction using **SHAP (SHapley Additive exPlanations)**, both per-patient (local) and model-wide (global).

Three roles, three views:
- **Patient** — run assessments, view history, download PDF reports
- **Doctor** — view any patient's assessment history
- **Admin** — system-wide stats and user management

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | FastAPI + SQLAlchemy + Alembic |
| Database | PostgreSQL |
| ML | scikit-learn (Random Forest) + SHAP |
| Auth | JWT + bcrypt |
| Testing | pytest |
| Deployment | Docker, Render (backend + DB), Vercel (frontend) |

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the system diagram and [`docs/er-diagram.md`](docs/er-diagram.md) for the database schema.

## Running locally

**Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
# create .env with DATABASE_URL and SECRET_KEY — see .env.example
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**Or, with Docker:**
```bash
docker-compose up --build
```

## Testing
```bash
cd backend
pytest -v
```

## Model Performance Summary

| Disease | Accuracy | Recall | ROC-AUC |
|---|---|---|---|
| Heart Disease | 86.7% | 82.1% | 94.6% |
| Breast Cancer | 95.6% | 97.2% | 99.3% |
| Kidney Disease | 100%* | 100%* | 100%* |
| Parkinson's | 92.3% | 96.6% | 96.6% |
| Lung Cancer | 91.9% | 94.4% | 94.2% |
| Liver Disease | 71.6% | 92.8% | 77.9% |
| Diabetes | 72.7% | 70.4%† | 82.7% |
| Thyroid | 94.0% | 76.7%† | 93.9% |
| Stroke | 75.2% | 59.5%† | 74.8% |
| Hepatitis | 93.8% | 100%‡ | 94.9% |

\* Small cleaned sample (n=203); consistent with published results on this dataset.
† Improved via SMOTE and/or threshold tuning to address class imbalance.
‡ Small test set (n=16); interpret with caution.

Full methodology and honest discussion of each model's limitations is in the project report.

## Known limitations
- Free-tier hosting means cold-start delays on first request
- Local and production databases are fully separate (no data sync)
- Model insights use scikit-learn's built-in feature importance (fast, model-specific) rather than a full SHAP-based global summary (computationally heavier at this scale)
- Lifestyle suggestions are informational only, not medical advice, and intentionally omitted for diseases with no genuinely modifiable risk factors (e.g. Breast Cancer, Parkinson's)

## License / Academic use
Built as a final year academic project.