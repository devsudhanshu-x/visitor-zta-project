async function loadLogs() {
  const res = await fetch("/audit/logs");
  if (!res.ok) return;
  const logs = await res.json();

  const body = document.getElementById("logBody");
  const empty = document.getElementById("logEmpty");

  if (logs.length === 0) {
    empty.style.display = "block";
    body.innerHTML = "";
    return;
  }

  empty.style.display = "none";
  body.innerHTML = logs.map(l => `
    <div class="log-row">
      <span class="log-time">${l.attempted_at}</span>
      <span class="mono">#${l.visit_id ?? "—"}</span>
      <span class="pill pill-${l.result}">${l.result.replace(/_/g, " ")}</span>
      <span class="log-reason">${l.reason ?? ""}</span>
    </div>
  `).join("");
}

loadLogs();
setInterval(loadLogs, 5000);