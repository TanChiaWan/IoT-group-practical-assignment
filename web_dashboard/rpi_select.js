
const table_name = document.getElementById('table-name').textContent;

const maxLength = 5;
let temperatureArray = [];
let intensityArray = [];
let humidityArray = [];


function getWeatherForecast() {
  const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=1.55&longitude=110.33&current_weather=true`;

  return fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      const currentWeather = data.current_weather;
      const hourlyForecast = data.hourly;

      console.log("Current Weather:", currentWeather);

      // Update the weather forecast div
      const weatherForecastDiv = document.getElementById("weatherForecast");
      weatherForecastDiv.innerHTML = `
        <h2>Current Weather</h2>
        <p>Temperature: <b>${currentWeather.temperature} °C</b></p>
        <p>Wind Speed: <b>${currentWeather.windspeed} km/h</b></p>
      `;

      // Check temperature and add recommendation
      if (currentWeather.temperature < 20) {
        const recommendation = document.createElement("p");
        recommendation.textContent = "Recommended to turn off the air-con";
        recommendation.style.fontWeight = "bold";
        recommendation.style.color = "blue";
        weatherForecastDiv.appendChild(recommendation);
      } else if (currentWeather.temperature >= 20 && currentWeather.temperature < 30) {
        const recommendation = document.createElement("p");
        recommendation.textContent = "Recommended to turn on the fans";
        recommendation.style.fontWeight = "bold";
        recommendation.style.color = "green";
        weatherForecastDiv.appendChild(recommendation);
      } else if (currentWeather.temperature >= 30) {
        const recommendation = document.createElement("p");
        recommendation.textContent = "Recommended to turn on the air-con";
        recommendation.style.fontWeight = "bold";
        recommendation.style.color = "red";
        weatherForecastDiv.appendChild(recommendation);
      }

      // Check wind speed and add recommendation
      if (currentWeather.windspeed >= 15) {
        const recommendation = document.createElement("p");
        recommendation.textContent = "Windy outside, recommended to open window";
        recommendation.style.fontWeight = "bold";
        recommendation.style.color = "orange";
        weatherForecastDiv.appendChild(recommendation);
      } else {
        const recommendation = document.createElement("p");
        recommendation.textContent = "Low wind, recommended to close window";
        recommendation.style.fontWeight = "bold";
        recommendation.style.color = "green";
        weatherForecastDiv.appendChild(recommendation);
      }

      return {
        currentWeather,
      };
    })
    .catch(error => {
      console.log("An error occurred:", error);
    });
}

getWeatherForecast()

// Get canvas elements
const ctx1 = document.getElementById('myChart').getContext('2d');
const ctx2 = document.getElementById('myChart2').getContext('2d');
const ctx3 = document.getElementById('myChart3').getContext('2d');

// Assuming the arrays contain direct values
// Convert the arrays to objects with 'time' and 'value' properties
const temperatureData = temperatureArray.map((value, index) => ({
  time: `Label ${index + 1}`,
  value: value
}));

const intensityData = intensityArray.map((value, index) => ({
  time: `Label ${index + 1}`,
  value: value
}));

const humidityData = humidityArray.map((value, index) => ({
  time: `Label ${index + 1}`,
  value: value
}));

// Chart data
const chartData1 = {
  labels: temperatureData.map(data => data.time),
  datasets: [{
    label: 'Temperature',
    data: temperatureData.map(data => data.value),
    borderColor: 'rgba(255, 99, 132, 1)',
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderWidth: 1
  }]
};

const chartData2 = {
  labels: intensityData.map(data => data.time),
  datasets: [{
    label: 'Light Intensity',
    data: intensityData.map(data => data.value),
    borderColor: 'rgba(54, 162, 235, 1)',
    backgroundColor: 'rgba(54, 162, 235, 0.2)',
    borderWidth: 1
  }]
};

const chartData3 = {
  labels: humidityData.map(data => data.time),
  datasets: [{
    label: 'Humidity',
    data: humidityData.map(data => data.value),
    borderColor: 'rgba(75, 192, 192, 1)',
    backgroundColor: 'rgba(75, 192, 192, 0.2)',
    borderWidth: 1
  }]
};

// Update chart options (unchanged)

// Update chart options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 100 // Maximum value for temperature chart (0-100)
    }
  }
};

const chartOptions2 = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 300 // Maximum value for light intensity chart (0-300)
    }
  }
};

const chartOptions3 = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 500 // Maximum value for humidity chart (0-500)
    }
  }
};

// Create charts
const chart1 = new Chart(ctx1, {
  type: 'line',
  data: chartData1,
  options: chartOptions
});

const chart2 = new Chart(ctx2, {
  type: 'line',
  data: chartData2,
  options: chartOptions2
});

const chart3 = new Chart(ctx3, {
  type: 'line',
  data: chartData3,
  options: chartOptions3
});


function mainElectClick() {
  var mainElecText = document.getElementById('mainElec_text');
  var currentText = mainElecText.textContent.trim();

  if (currentText === "Main Electricity: OFF") {
    mainElecText.textContent = 'Main Electricity: ON';

  }
  else {
    mainElecText.textContent = 'Main Electricity: OFF';

  }

  sendButtonText({
    buttonText: mainElecText.textContent,
    table: table_name
  });
}

function punitiveClick() {
  var punitiveText = document.getElementById('punitive_text');
  var currentText = punitiveText.textContent.trim();

  if (currentText === "Punitive Mechanism: OFF") {
    punitiveText.textContent = 'Punitive Mechanism: ON';

  }
  else {
    punitiveText.textContent = 'Punitive Mechanism: OFF';

  }

  sendButtonText({
    buttonText: punitiveText.textContent,
    table: table_name
  });
}

function fetchData() {
  fetch('/latest_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ table_name: table_name })
  })
    .then(response => response.json())
    .then(data => {
      console.log("Data is fetched");
      console.log(data);
      document.getElementById("latest-electric").textContent = data.electricityStatus;
      document.getElementById("latest-airCon").textContent = data.airCondStatus;
      document.getElementById("latest-noise").textContent = data.noiseLevel;
      document.getElementById("latest-light").textContent = data.lightStatus;
      document.getElementById("latest-lightIntensity").textContent = data.lightIntensity;
      document.getElementById("latest-temp").textContent = data.temperature;
      document.getElementById("latest-humidity").textContent = data.humidity;
      
      const currentTime = new Date().toLocaleTimeString();

      // Insert temperature into the array after a minute
      if (temperatureArray.length < maxLength) {
        temperatureArray.push({ time: currentTime, value: data.temperature });
      } else {
        temperatureArray.shift();
        temperatureArray.push({ time: currentTime, value: data.temperature });
      }
    
      // Insert light intensity into the array after a minute
      if (intensityArray.length < maxLength) {
        intensityArray.push({ time: currentTime, value: data.lightIntensity });
      } else {
        intensityArray.shift();
        intensityArray.push({ time: currentTime, value: data.lightIntensity });
      }
    
      // Insert humidity into the array after a minute
      if (humidityArray.length < maxLength) {
        humidityArray.push({ time: currentTime, value: data.humidity });
      } else {
        humidityArray.shift();
        humidityArray.push({ time: currentTime, value: data.humidity });
      }
    
      // Update chart data
      chartData1.labels = temperatureArray.map(data => data.time);
      chartData1.datasets[0].data = temperatureArray.map(data => data.value);
    
      chartData2.labels = intensityArray.map(data => data.time);
      chartData2.datasets[0].data = intensityArray.map(data => data.value);
    
      chartData3.labels = humidityArray.map(data => data.time);
      chartData3.datasets[0].data = humidityArray.map(data => data.value);
    
      // Update the charts
      chart1.update();
      chart2.update();
      chart3.update();
      
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function sendButtonText(buttonText) {
  fetch('/button_text', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(buttonText)
  })
    .then(response => {
      console.log('Button text sent successfully.');
    })
    .catch(error => {
      console.error('Error:', error);
    });
}


fetchData();

setInterval(fetchData, 3000);