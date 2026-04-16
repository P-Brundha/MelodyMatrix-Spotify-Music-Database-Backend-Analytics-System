const API_BASE = "http://127.0.0.1:8000";

function renderTable(rows) {
  if (!rows || rows.length === 0) return "<p>No rows</p>";
  const keys = Object.keys(rows[0]);
  let html = "<table><thead><tr>";
  for (const k of keys) html += `<th>${k}</th>`;
  html += "</tr></thead><tbody>";
  for (const r of rows) {
    html += "<tr>";
    for (const k of keys) html += `<td>${r[k] ?? ""}</td>`;
    html += "</tr>";
  }
  html += "</tbody></table>";
  return html;
}

document.getElementById("btn-artists").addEventListener("click", async () => {
  document.getElementById("output").innerHTML = "<p>Loading artists...</p>";
  const res = await fetch(`${API_BASE}/artists?limit=200`);
  const data = await res.json();
  document.getElementById("output").innerHTML = `<h2>Artists</h2>` + renderTable(data);
});

document.getElementById("btn-tracks").addEventListener("click", async () => {
  document.getElementById("output").innerHTML = "<p>Loading tracks...</p>";
  const res = await fetch(`${API_BASE}/tracks?limit=200`);
  const data = await res.json();
  document.getElementById("output").innerHTML = `<h2>Tracks</h2>` + renderTable(data);
});

document.getElementById("btn-top").addEventListener("click", async () => {
  document.getElementById("output").innerHTML = "<p>Loading top tracks...</p>";
  const res = await fetch(`${API_BASE}/top-tracks`);
  const data = await res.json();
  document.getElementById("output").innerHTML = `<h2>Top Tracks</h2>` + renderTable(data);
});
