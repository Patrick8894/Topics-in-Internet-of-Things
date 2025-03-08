const net = require('net');

var server_port = 65432;
var server_addr = "172.20.10.3";   // the IP address of your Raspberry PI

const client = net.createConnection({ port: server_port, host: server_addr }, () => {
    // 'connect' listener.
    console.log('connected to server!');
});

client.on('error', (err) => {
    console.error('Connection error:', err.message);
    document.getElementById("error").innerText = 'Connection error: ' + err.message;
});

function sendMessage(message) {
    client.write(message);
}

function control(direction) {
    console.log("Control: " + direction);
    sendMessage(direction);
    sendMessage("getCarInfo");
}

// Function to send a request to the server periodically
function updateCarInfo() {
    setInterval(() => {
        sendMessage("getCarInfo");
    }, 10000);
}

client.on('data', (data) => {
    try {
        const jsonData = JSON.parse(data);
        console.log(jsonData);
        // Update the DOM with the parsed JSON data
        document.getElementById("battery").innerText = jsonData.battery;
        document.getElementById("movingDirection").innerText = jsonData.movingDirection;
        document.getElementById("turning").innerText = jsonData.turning;
        document.getElementById("cpu_temperature").innerText = jsonData.cpu_temperature;
    } catch (e) {
        console.error("Failed to parse JSON:", e);
    }
});

client.on('end', () => {
    console.log('disconnected from server');
});

sendMessage("getCarInfo")
updateCarInfo();