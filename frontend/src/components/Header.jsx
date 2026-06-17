export default function Header() {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="brand">
          <div className="brand-icon">⚙</div>
          <div>
            <h1 className="brand-title">ResumeAI Screener</h1>
            <p className="brand-subtitle">TF-IDF · Cosine Similarity · NLP-Powered Ranking</p>
          </div>
        </div>
        <div className="header-badge">AI-Powered</div>
      </div>
    </header>
  );
}