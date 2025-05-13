const deviceId = window.location.pathname.split("/").pop();

async function fetchHistory() {
  const res = await fetch(`/api/history/${deviceId}`);
  const data = await res.json();

  const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString());
  const temps = data.map(d => d.temperature);
  const hums = data.map(d => d.humidity);
  const sounds = data.map(d => d.sound);

  const ctxTemp = document.getElementById("chartTemp").getContext("2d");
  new Chart(ctxTemp, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Temperature (°C)",
        data: temps,
        borderColor: "rgba(255, 99, 132, 1)",  // Red
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        tension: 0.2
      }]
    }
  });

  const ctxHum = document.getElementById("chartHumidity").getContext("2d");
  new Chart(ctxHum, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Humidity (%)",
        data: hums,
        borderColor: "rgba(54, 162, 235, 1)",  // Blue
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        tension: 0.2
      }]
    }
  });

  const ctxSound = document.getElementById("chartSound").getContext("2d");
  new Chart(ctxSound, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Sound (dB)",
        data: sounds,
        borderColor: "rgba(255, 206, 86, 1)",  // Yellow
        backgroundColor: "rgba(255, 206, 86, 0.2)",
        tension: 0.2
      }]
    }
  });
}

fetchHistory();
