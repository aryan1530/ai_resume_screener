import { useState } from "react";
import ResumeCard from "./ResumeCard";

export default function ResultsPanel({ results, warnings }) {
  const [expanded, setExpanded] = useState(null);

  const toggle = (id) => setExpanded((prev) => (prev === id ? null : id));

  return (
    <section className="results-panel">
      <div className="results-header">
        <h2 className="results-title">Ranked Results</h2>
        <p className="results-sub">Sorted by cosine similarity to the job description</p>
      </div>

      {warnings && warnings.length > 0 && (
        <div className="warnings-box">
          <strong>Parse warnings:</strong>
          <ul>
            {warnings.map((w, i) => <li key={i}>{w}</li>)}
          </ul>
        </div>
      )}

      <div className="results-list">
        {results.map((resume) => (
          <ResumeCard
            key={resume.id}
            resume={resume}
            isExpanded={expanded === resume.id}
            onToggle={() => toggle(resume.id)}
          />
        ))}
      </div>
    </section>
  );
}