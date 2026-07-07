export default function InputForm({ values, onChange, onSubmit, loading }) {
  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5 rounded-3xl border border-white/10 bg-white/8 p-6 shadow-glow backdrop-blur-xl">
      <div className="grid gap-5 md:grid-cols-3">
        <label className="space-y-2 text-sm text-slate-300">
          <span className="block font-medium text-slate-100">Task completion time</span>
          <input
            type="number"
            min="0.5"
            step="0.1"
            value={values.task_completion_time_hours}
            onChange={(event) => onChange('task_completion_time_hours', event.target.value)}
            className="w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-slate-100 outline-none transition focus:border-teal-400 focus:ring-2 focus:ring-teal-400/30"
            placeholder="6.5"
          />
          <span className="text-xs text-slate-400">Hours spent on the assigned task</span>
        </label>

        <label className="space-y-2 text-sm text-slate-300">
          <span className="block font-medium text-slate-100">Feedback rating</span>
          <input
            type="number"
            min="1"
            max="5"
            step="0.1"
            value={values.feedback_rating}
            onChange={(event) => onChange('feedback_rating', event.target.value)}
            className="w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-slate-100 outline-none transition focus:border-amber-400 focus:ring-2 focus:ring-amber-400/30"
            placeholder="4.2"
          />
          <span className="text-xs text-slate-400">Mentor or manager score from 1 to 5</span>
        </label>

        <label className="space-y-2 text-sm text-slate-300">
          <span className="block font-medium text-slate-100">Attendance percentage</span>
          <input
            type="number"
            min="0"
            max="100"
            step="0.1"
            value={values.attendance_percentage}
            onChange={(event) => onChange('attendance_percentage', event.target.value)}
            className="w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-slate-100 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/30"
            placeholder="92"
          />
          <span className="text-xs text-slate-400">Attendance window across the internship period</span>
        </label>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="max-w-xl text-sm leading-6 text-slate-400">
          This demo predicts a score and category from productivity, feedback, and attendance signals.
        </p>
        <button
          type="submit"
          disabled={loading}
          className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-teal-400 via-cyan-400 to-amber-400 px-6 py-3 font-semibold text-slate-950 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Predicting...' : 'Predict performance'}
        </button>
      </div>
    </form>
  );
}
