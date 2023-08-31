// chart.js
// Вам нужно иметь доступ к isSimulationRunning из simulation.js
// Подключите файл simulation.js перед этим файлом

const stopButton = document.getElementById('stop-button'); // Замените на соответствующий ID кнопки

stopButton.addEventListener('click', () => {
  stopSimulation(); // Вызов функции из simulation.js
  console.log('simulation stopped');
});

