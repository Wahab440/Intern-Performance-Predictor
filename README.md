# Intern Performance Predictor

End-to-end demo for predicting intern performance from three operational signals: task completion time, feedback rating, and attendance percentage.

## What this project does

The backend trains a regression model on simulated intern data, then converts the numeric score into three review-friendly categories:

- `score >= 80` -> `Excellent`
- `50 <= score < 80` -> `Average`
- `score < 50` -> `Struggling`

The API serves predictions through FastAPI, and the React frontend provides a simple dashboard for score lookup and category display. A MongoDB connection is included as an optional demo log store for prediction history.

## Project Layout

- `backend/app/train.py` generates or loads intern data, cleans it, engineers features, trains the regressor, and saves the artifact.
- `backend/app/main.py` exposes `GET /health` and `POST /predict`.
- `frontend/src/pages/Dashboard.jsx` renders the UI and connects to the API.

## ML Approach

I used `RandomForestRegressor` because this is a tabular problem with small-to-medium synthetic data and non-linear relationships between the inputs and the target score. Random Forest is easy to train, robust to feature interactions, and gives usable feature importance values for review.

Feature engineering adds:

- `efficiency_index` = feedback rating scaled by task speed
- `attendance_strength` = attendance normalized to a `0-1` range
- `feedback_attendance_interaction` = interaction term between mentor feedback and attendance

The training script reports RMSE on a holdout split and exports feature importance from the fitted model.

## Real Intern Evaluation Mapping

This demo maps common internship review signals to a performance score:

- Task completion time reflects delivery speed and execution discipline.
- Feedback rating captures mentor review quality and task correctness.
- Attendance percentage approximates reliability and engagement.

In a real system, this could be extended with rubric-based milestones, code review quality, incident response, peer feedback, and project outcomes.

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m app.train
uvicorn app.main:app --reload --port 8000
```

### API

- `POST /predict`

  Request body:

  ```json
  {
    "task_completion_time_hours": 6.5,
    "feedback_rating": 4.2,
    "attendance_percentage": 91
  }
  ```

- `GET /health`

## MongoDB Demo Logging

If `MONGODB_URI` is set, every prediction is written to the configured collection.

Environment variables:

- `MONGODB_URI`
- `MONGODB_DB` default: `intern_performance`
- `MONGODB_COLLECTION` default: `predictions`

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

If the API is not on `http://localhost:8000`, set `VITE_API_BASE_URL` in the frontend environment.

## Deployment

Recommended setup:

- Backend: Railway free tier using [backend/railway.toml](backend/railway.toml)
- Frontend: Vercel static site from the `frontend` folder

Backend deployment steps on Railway:

1. Create a new project from the GitHub repo.
2. Set the service root to `backend`.
3. Set `MONGODB_URI` only if you want prediction logging.
4. Deploy and copy the public backend URL.

Railway will use the backend `railway.toml` file and start the FastAPI app on `$PORT`.

If Railway still generates a default build step, set the service build command to `python -m pip install -r requirements.txt`.

Frontend deployment steps on Vercel:

1. Import the same GitHub repo.
2. Set the project root to `frontend`.
3. Add `VITE_API_BASE_URL` with the deployed backend URL.
4. Deploy the site.

The frontend already includes a [Vercel config](frontend/vercel.json) so client-side routes resolve to `index.html`.

Use the example environment files if you want a quick template:

- [backend/.env.example](backend/.env.example)
- [frontend/.env.example](frontend/.env.example)

If you prefer a simpler single-provider setup, you can host the frontend on Vercel and point it to the Railway backend URL through `VITE_API_BASE_URL`.

Local deployment-style test:

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

cd ../frontend
npm run build
```

## Why this is hiring-manager friendly

- Clean separation between training, inference, and presentation layers.
- Type-annotated Python backend with a single prediction contract.
- Feature engineering and evaluation are explicit and easy to review.
- Frontend is intentionally simple but fully connected to the API.
- The stack is realistic for an internship evaluation workflow and easy to extend into production.
