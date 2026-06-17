export default function StatsBar({ stats, total, job }) {
  if (!stats || Object.keys(stats).length === 0) return null;

  return (
    <div className="stats-bar">
      <div className="stats-job">
        <span className="stats-label">Screening for</span>
        <span className="stats-job-title">{job?.title}</span>
      </div>
      <div className="stats-grid">
        <div className="stat-item">
          <span className="stat-value">{total}</span>
          <span className="stat-label">Resumes Screened</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.max}%</span>
          <span className="stat-label">Top Score</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.mean}%</span>
          <span className="stat-label">Average Score</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.min}%</span>
          <span className="stat-label">Lowest Score</span>
        </div>
      </div>
    </div>
  );
}