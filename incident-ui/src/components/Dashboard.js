export default function Dashboard({ incidents, selected, onSelect, onNewClick }) {
  const active = incidents.filter(i => i.status === "active").length;
  const resolved = incidents.filter(i => i.status === "resolved").length;
  const critical = incidents.filter(i => i.severity === "critical").length;

  return (
    <div className="page">
      <div className="page-title">Incident Dashboard</div>
      <div className="page-sub">Real-time overview of all incidents</div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: 24 }}>
        {[
          { label: "Active", value: active, color: "#ff4444" },
          { label: "Resolved Today", value: resolved, color: "#6affb0" },
          { label: "Critical", value: critical, color: "#ff8c42" },
        ].map(m => (
          <div key={m.label} className="card" style={{ textAlign: "center", padding: "20px" }}>
            <div style={{ fontSize: 36, fontWeight: 800, color: m.color }}>{m.value}</div>
            <div style={{ fontSize: 13, color: "#6b6b8a", marginTop: 4 }}>{m.label}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="card-title">All Incidents</div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <thead>
            <tr style={{ borderBottom: "1px solid #2a2a3a" }}>
              {["ID", "Title", "Severity", "Type", "Time", "Status"].map(h => (
                <th key={h} style={{ padding: "8px 12px", textAlign: "left", color: "#6b6b8a", fontWeight: 500, fontSize: 12 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {incidents.map(inc => (
              <tr key={inc.id} onClick={() => onSelect(inc)} style={{ borderBottom: "1px solid #1a1a24", cursor: "pointer", background: selected?.id === inc.id ? "#1a1a24" : "transparent", transition: "background 0.1s" }}>
                <td style={{ padding: "10px 12px", fontFamily: "JetBrains Mono, monospace", fontSize: 12, color: "#6b6b8a" }}>{inc.id}</td>
                <td style={{ padding: "10px 12px", fontWeight: 500 }}>{inc.title}</td>
                <td style={{ padding: "10px 12px" }}><span className={`badge badge-${inc.severity}`}>{inc.severity}</span></td>
                <td style={{ padding: "10px 12px", color: "#6b6b8a", fontSize: 13 }}>{inc.type}</td>
                <td style={{ padding: "10px 12px", color: "#6b6b8a", fontSize: 13 }}>{inc.time}</td>
                <td style={{ padding: "10px 12px" }}>
                  <span style={{ fontSize: 12, color: inc.status === "active" ? "#ff6a6a" : "#6affb0" }}>
                    {inc.status === "active" ? "● Active" : "✓ Resolved"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <button className="btn btn-primary" onClick={onNewClick}>＋ Report New Incident</button>
    </div>
  );
}