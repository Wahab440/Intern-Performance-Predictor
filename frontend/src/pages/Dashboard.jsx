import { useEffect, useMemo, useState } from 'react';
import InputForm from '../components/InputForm';
import { getHealth, predictPerformance } from '../services/api';

const initialValues = {
  task_completion_time_hours: '6.5',
  feedback_rating: '4.2',
  attendance_percentage: '91',
};

const badgeStyles = {
  Excellent: 'bg-emerald-400/15 text-emerald-300 ring-1 ring-emerald-400/30',
  Average: 'bg-amber-400/15 text-amber-200 ring-1 ring-amber-400/30',
  Struggling: 'bg-rose-400/15 text-rose-200 ring-1 ring-rose-400/30',
};

function formatPercentage(value) {
  return `${Math.round(value)}%`;
}

export default function Dashboard() {
  const [values, setValues] = useState(initialValues);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [health, setHealth] = useState('checking');
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    getHealth()
      .then((response) => {
        if (active) {
          setHealth(response.model_ready ? 'ready' : 'degraded');
        }
      })
      .catch(() => {
        if (active) {
          setHealth('offline');
        }
      });
    return () => {
      active = false;
    };
  }, []);

  const score = result?.predicted_score ?? 0;
  const label = result?.performance_label ?? 'Awaiting input';

  const meterStyle = useMemo(
    () => ({ background: `conic-gradient(#14b8a6 ${score * 3.6}deg, rgba(255,255,255,0.08) 0deg)` }),
    [score],
  );

  const handleChange = (field, value) => {
    setValues((current) => ({ ...current, [field]: value }));
  };

  const handlePredict = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await predictPerformance({
        task_completion_time_hours: Number(values.task_completion_time_hours),
        feedback_rating: Number(values.feedback_rating),
        attendance_percentage: Number(values.attendance_percentage),
      });
      setResult(response);
    } catch (requestError) {
      setError(requestError.message || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-hero-radial">
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8 lg:py-14">
        <section className="mb-8 grid gap-6 lg:grid-cols-[1.3fr_0.7fr] lg:items-end">
          <div className="space-y-5">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.28em] text-slate-300">
              Intern Performance Predictor
            </div>
            <div className="space-y-4">
              <h1 className="max-w-3xl text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl">
                Predict intern performance with a production-style ML demo.
              </h1>
              <p className="max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
                Use task completion time, feedback ratings, and attendance to estimate a score and categorize each intern as Excellent, Average, or Struggling.
              </p>
            </div>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/6 p-5 shadow-glow backdrop-blur-xl">
            <div className="flex items-center justify-between text-sm text-slate-300">
              <span>Service status</span>
              <span
                className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] ${
                  health === 'ready'
                    ? 'bg-emerald-400/15 text-emerald-300'
                    : health === 'checking'
                      ? 'bg-slate-400/15 text-slate-200'
                      : 'bg-rose-400/15 text-rose-200'
                }`}
              >
                {health}
              </span>
            </div>
            <div className="mt-5 grid gap-4 sm:grid-cols-2">
              <div className="rounded-2xl border border-white/10 bg-slate-950/45 p-4">
                <p className="text-sm text-slate-400">Predicted score</p>
                <p className="mt-2 text-3xl font-bold text-white">{result ? score.toFixed(1) : '--'}</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-slate-950/45 p-4">
                <p className="text-sm text-slate-400">Performance label</p>
                <p className="mt-2 text-3xl font-bold text-white">{label}</p>
              </div>
            </div>
          </div>
        </section>

        <InputForm values={values} onChange={handleChange} onSubmit={handlePredict} loading={loading} />

        {error ? (
          <div className="mt-5 rounded-2xl border border-rose-400/25 bg-rose-400/10 px-4 py-3 text-sm text-rose-100">
            {error}
          </div>
        ) : null}

        <section className="mt-6 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
          <div className="rounded-3xl border border-white/10 bg-white/6 p-6 shadow-glow backdrop-blur-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.25em] text-slate-400">Performance badge</p>
                <h2 className="mt-2 text-2xl font-bold text-white">{label}</h2>
              </div>
              <span className={`rounded-full px-4 py-2 text-sm font-semibold ${badgeStyles[label] ?? 'bg-slate-400/15 text-slate-200 ring-1 ring-white/20'}`}>
                {label}
              </span>
            </div>

            <div className="mt-8 flex items-center gap-6">
              <div className="relative flex h-40 w-40 items-center justify-center rounded-full" style={meterStyle}>
                <div className="flex h-28 w-28 flex-col items-center justify-center rounded-full border border-white/10 bg-slate-950 text-center">
                  <span className="text-3xl font-bold text-white">{result ? score.toFixed(0) : '0'}</span>
                  <span className="text-xs uppercase tracking-[0.22em] text-slate-400">out of 100</span>
                </div>
              </div>
              <div className="space-y-3 text-sm text-slate-300">
                <p className="leading-6 text-slate-300">
                  Higher scores correspond to strong completion speed, positive feedback, and consistent attendance.
                </p>
                <p className="leading-6 text-slate-400">
                  The backend returns a regression score first and then maps it into the three hiring-manager friendly categories.
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/6 p-6 shadow-glow backdrop-blur-xl">
            <p className="text-sm uppercase tracking-[0.25em] text-slate-400">Score chart</p>
            <h2 className="mt-2 text-2xl font-bold text-white">Normalized performance gauge</h2>
            <div className="mt-8 space-y-5">
              <div>
                <div className="mb-2 flex items-center justify-between text-sm text-slate-400">
                  <span>Predicted score</span>
                  <span>{result ? formatPercentage(score) : '0%'}</span>
                </div>
                <div className="h-4 overflow-hidden rounded-full bg-white/8">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-teal-400 via-cyan-400 to-amber-400 transition-all duration-500"
                    style={{ width: `${Math.max(0, Math.min(100, score))}%` }}
                  />
                </div>
              </div>

              <div className="grid gap-4 sm:grid-cols-3">
                <div className="rounded-2xl border border-white/10 bg-slate-950/45 p-4">
                  <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Task time</p>
                  <p className="mt-2 text-xl font-semibold text-white">{values.task_completion_time_hours} hrs</p>
                </div>
                <div className="rounded-2xl border border-white/10 bg-slate-950/45 p-4">
                  <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Feedback</p>
                  <p className="mt-2 text-xl font-semibold text-white">{values.feedback_rating}/5</p>
                </div>
                <div className="rounded-2xl border border-white/10 bg-slate-950/45 p-4">
                  <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Attendance</p>
                  <p className="mt-2 text-xl font-semibold text-white">{values.attendance_percentage}%</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
