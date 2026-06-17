function ScoreBar({ score }) {
  const color =
    score >= 70 ? "#22c55e" : score >= 45 ? "#f59e0b" : "#ef4444";

  return (
    <div className="score-bar-wrap">
      <div className="score-bar-track">
        <div
          className="score-bar-fill"
          style={{ width: `${Math.min(score, 100)}%`, backgroundColor: color }}
        />
      </div>
      <span className="score-percent" style={{ color }}>
        {score.toFixed(1)}%
      </span>
    </div>
  );
}

function RankBadge({ rank }) {
  const medals = { 1: "🥇", 2: "🥈", 3: "🥉" };
  return (
    <div className={`rank-badge rank-badge--${rank <= 3 ? rank : "default"}`}>
      {medals[rank] || `#${rank}`}
    </div>
  );
}

export default function ResumeCard({ resume, isExpanded, onToggle }) {
  const { candidate_name, filename, score, matched_keywords, rank, preview } = resume;

  return (
    <div className={`resume-card ${rank === 1 ? "resume-card--top" : ""}`}>
      <div className="resume-card-main" onClick={onToggle}>
        <RankBadge rank={rank} />
        <div className="resume-info">
          <div className="resume-name">{candidate_name}</div>
          <div className="resume-filename">{filename}</div>
          <ScoreBar score={score} />
        </div>
        <div className="resume-meta">
          <div className="keywords-count">
            <strong>{matched_keywords.length}</strong> keyword{matched_keywords.length !== 1 ? "s" : ""} matched
          </div>
          <button className="expand-btn">{isExpanded ? "▲ Collapse" : "▼ Details"}</button>
        </div>
      </div>

      {isExpanded && (
        <div className="resume-card-detail">
          {matched_keywords.length > 0 && (
            <div className="keyword-section">
              <h4 className="detail-label">Matched Keywords</h4>
              <div className="keyword-chips">
                {matched_keywords.map((kw) => (
                  <span key={kw} className="chip">{kw}</span>
                ))}
              </div>
            </div>
          )}
          <div className="preview-section">
            <h4 className="detail-label">Resume Preview</h4>
            <p className="preview-text">{preview}</p>
          </div>
        </div>
      )}
    </div>
  );
}