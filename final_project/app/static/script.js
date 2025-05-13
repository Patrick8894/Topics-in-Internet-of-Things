async function fetchData() {
  const res = await fetch('/api/data');
  const data = await res.json();

  console.log(data); // you can replace this with charting later
  const chart = document.getElementById('chart');
  data.forEach(entry => {
    const p = document.createElement('p');
    p.textContent = `⏱ ${entry.timestamp} | 🌡️ ${entry.temperature}°C | 💧 ${entry.humidity}% | 🔊 ${entry.sound}dB`;
    chart.appendChild(p);
  });
}

fetchData();
