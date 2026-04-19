import { useState } from "react";

export default function IncidentForm({ onSubmit, loading }) {
  const [form, setForm] = useState({ incident_id: "", title: "", description: "", severity: "high" });

  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = (e) => {
    e.preventDefault();
    if (!form.incident_id || !form.title || !form.description) return;
    onSubmit(form);
  };

  const inputStyle = { width: "100%", padding: "10px 14px", background: "#111118", border: "1px solid #2a2a3a", borderRadius: 8, color: "#e8e8f0", fontFamily: "Syne, sans-serif", fontSize: 14, outline: "none", marginTop: 6 };
  const labelStyle = { fontSize: 13, color: "#6b6b8a", fontWeight: 500 };

  return (
    <div className="page">
      <div className="page-title">Report Incident</div>
      <div className="page-sub">Fill in the details — the AI agent will analyze and respond</div>

      <div className="card">
        <form onSubmit={submit} style={{ display: "flex", flexDirection: "column", gap: 18 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div>
              <label style={labelStyle}>Incident ID</label>
              <input name="incident_id" value={form.incident_id} onChange={handle} placeholder="e.g. INC-005" style={inputStyle} required />
            </div>
            <div>
              <label style={labelStyle}>Severity</label>
              <select name="severity" value={form.severity} onChange={handle} style={inputStyle}>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
          </div>

          <div>
            <label style={labelStyle}>Incident Title</label>
            <input name="title" value={form.title} onChange={handle} placeholder="e.g. Payment service down" style={inputStyle} required />
          </div>

          <div>
            <label style={labelStyle}>Description</label>
            <textarea name="description" value={form.description} onChange={handle} placeholder="Describe what is happening in detail..." style={{ ...inputStyle, minHeight: 120, resize: "vertical" }} required />
          </div>

          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            {["Database connection pool exhausted, 503 errors", "SSH brute force attack on production server", "Disk usage at 95% on prod-db-01", "API latency spike in EU region"].map(s => (
              <button key={s} type="button" onClick={() => setForm({ ...form, description: s })}
                style={{ padding: "6px 12px", background: "#1a1a24", border: "1px solid #2a2a3a", borderRadius: 6, color: "#6b6b8a", fontSize: 12, cursor: "pointer", fontFamily: "Syne, sans-serif" }}>
                {s.slice(0, 30)}...
              </button>
            ))}
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading} style={{ alignSelf: "flex-start", padding: "12px 28px" }}>
            {loading ? "Analyzing..." : "⚡ Analyze with AI"}
          </button>
        </form>
      </div>
    </div>
  );
}