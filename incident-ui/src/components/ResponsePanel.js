export default function ResponsePanel({ response, loading }) {
  if (loading) return (
    <div className="page" style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "60vh", gap: 16 }}>
      <div style={{ width: 48, height: 48, border: "3px solid #2a2a3a", borderTop: "3px solid #7c6aff", borderRadius: "50%", animation: "spin 1s linear infinite" }}></div>
      <div style={{ color: "#6b6b8a", fontSize: 14 }}>AI Agent is analyzing the incident...</div>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );

  if (!response) return (
    <div className="page" style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "60vh", gap: 12 }}>
      <div style={{ fontSize: 48 }}>◎</div>
      <div style={{ color: "#6b6b8a", fontSize: 14 }}>No analysis yet. Submit an incident to see results.</div>
    </div>
  );

  if (response.error) return (
    <div className="page">
      <div className="card" style={{ borderColor: "#ff4444" }}>
        <div style={{ color: "#ff4444", fontWeight: 700, marginBottom: 8 }}>Error</div>
        <div style={{ color: "#6b6b8a", fontSize: 14 }}>{response.error}</div>
      </div>
    </div>
  );

  return (
    <div className="page">
      <div className="page-title">AI Analysis</div>
      <div className="page-sub">Incident ID: {response.incident_id}</div>

      <div className="card">
        <div className="card-title">Analysis Report</div>
        <div style={{ fontSize: 14, lineHeight: 1.8, color: "#c8c8d8", whiteSpace: "pre-wrap", fontFamily: "JetBrains Mono, monospace" }}>
          {response.analysis}
        </div>
      </div>

      <button className="btn btn-primary" onClick={() => window.history.back()}>← New Incident</button>
    </div>
  );
}