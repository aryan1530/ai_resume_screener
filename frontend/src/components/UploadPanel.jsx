import { useState, useRef } from "react";
import { screenResumes, fetchSampleJD } from "../services/api";

export default function UploadPanel({ onComplete, onError, onReset, setLoading, loading, hasResults }) {
  const [jobTitle, setJobTitle] = useState("");
  const [jobDesc, setJobDesc] = useState("");
  const [files, setFiles] = useState([]);
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef();

  const handleSampleJD = async () => {
    try {
      const data = await fetchSampleJD();
      setJobTitle(data.title);
      setJobDesc(data.description);
    } catch {
      onError("Could not load sample job description.");
    }
  };

  const handleFiles = (incoming) => {
    const valid = Array.from(incoming).filter(
      (f) => f.name.endsWith(".pdf") || f.name.endsWith(".txt")
    );
    setFiles((prev) => {
      const existing = new Set(prev.map((f) => f.name));
      return [...prev, ...valid.filter((f) => !existing.has(f.name))];
    });
  };

  const removeFile = (name) => setFiles((prev) => prev.filter((f) => f.name !== name));

  const handleSubmit = async () => {
    if (!jobTitle.trim() || !jobDesc.trim() || files.length === 0) {
      onError("Please fill in the job title, description, and upload at least one resume.");
      return;
    }
    setLoading(true);
    try {
      const data = await screenResumes(jobTitle, jobDesc, files);
      onComplete(data);
    } catch (err) {
      onError(err.message || "Screening failed. Is the Python API running on port 5000?");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setJobTitle("");
    setJobDesc("");
    setFiles([]);
    onReset();
  };

  return (
    <section className="upload-panel">
      <div className="panel-grid">
        <div className="card">
          <div className="card-header">
            <span className="card-step">01</span>
            <h2 className="card-title">Job Description</h2>
            <button className="btn-ghost" onClick={handleSampleJD} type="button">
              Load Sample
            </button>
          </div>
          <input
            className="input"
            type="text"
            placeholder="Job Title (e.g. Senior Python Developer)"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
          />
          <textarea
            className="textarea"
            placeholder="Paste the full job description here..."
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            rows={10}
          />
          <div className="char-count">{jobDesc.length} characters</div>
        </div>

        <div className="card">
          <div className="card-header">
            <span className="card-step">02</span>
            <h2 className="card-title">Upload Resumes</h2>
            <span className="badge">{files.length} file{files.length !== 1 ? "s" : ""}</span>
          </div>

          <div
            className={`drop-zone ${dragging ? "drop-zone--active" : ""}`}
            onClick={() => fileInputRef.current.click()}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={(e) => { e.preventDefault(); setDragging(false); handleFiles(e.dataTransfer.files); }}
          >
            <div className="drop-icon">📄</div>
            <p className="drop-label">Drop PDF or TXT files here</p>
            <p className="drop-sub">or click to browse</p>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".pdf,.txt"
              style={{ display: "none" }}
              onChange={(e) => handleFiles(e.target.files)}
            />
          </div>

          {files.length > 0 && (
            <ul className="file-list">
              {files.map((f) => (
                <li key={f.name} className="file-item">
                  <span className="file-icon">{f.name.endsWith(".pdf") ? "📕" : "📝"}</span>
                  <span className="file-name">{f.name}</span>
                  <span className="file-size">{(f.size / 1024).toFixed(1)} KB</span>
                  <button className="file-remove" onClick={() => removeFile(f.name)}>✕</button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="actions">
        <button className="btn-secondary" onClick={handleReset} disabled={loading}>
          Reset
        </button>
        <button className="btn-primary" onClick={handleSubmit} disabled={loading}>
          {loading ? (
            <><span className="spinner" /> Analyzing Resumes…</>
          ) : (
            "▶  Run AI Screening"
          )}
        </button>
      </div>
    </section>
  );
}