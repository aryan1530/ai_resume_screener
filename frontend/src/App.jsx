import { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import ResultsPanel from "./components/ResultsPanel";
import Header from "./components/Header";
import StatsBar from "./components/StatsBar";
import "./App.css";

export default function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleScreeningComplete = (data) => {
    setResults(data);
    setError(null);
  };

  const handleError = (msg) => {
    setError(msg);
    setResults(null);
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <UploadPanel
          onComplete={handleScreeningComplete}
          onError={handleError}
          onReset={handleReset}
          setLoading={setLoading}
          loading={loading}
          hasResults={!!results}
        />
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠</span> {error}
          </div>
        )}
        {results && (
          <>
            <StatsBar stats={results.stats} total={results.total_screened} job={results.job} />
            <ResultsPanel results={results.results} warnings={results.parse_warnings} />
          </>
        )}
      </main>
    </div>
  );
}