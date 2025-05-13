async function loadLatest() {
  const res = await fetch("/api/latest");
  const data = await res.json();
  const container = document.getElementById("latest");

  data.forEach(d => {
    const div = document.createElement("div");
    div.innerHTML = `
      <h3>Device: ${d.device_id}</h3>
      <p>🌡 Temperature: ${d.temperature} °C</p>
      <p>💧 Humidity: ${d.humidity} %</p>
      <p>🔊 Sound: ${d.sound} dB</p>
      <p>⏱ Timestamp: ${new Date(d.timestamp).toLocaleString()}</p>
      <a href="/device/${d.device_id}">🔍 View history</a>
      <hr />
    `;
    container.appendChild(div);
  });
}
loadLatest();
