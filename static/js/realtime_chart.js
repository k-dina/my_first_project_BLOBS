
var ctx = document.getElementById('realtimeChart').getContext('2d');
var step = last_step;
var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Array(10).fill(''), // Начальное заполнение пустыми метками
        datasets: [{
            label: 'Real-time Data',
            data: Array(10).fill(null), // Начальное заполнение null значениями
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        animation: false, // Отключение стандартной анимации Chart.js
        responsive: true,
        scales: {
            x: {
                display: true
            },
            y: {
                beginAtZero: true
            }
        }
    }
});


function shiftChartData(newData) {
    var labels = chart.data.labels;
    var values = chart.data.datasets[0].data;

    labels.shift(); // Удаление первой метки
    values.shift(); // Удаление первого значения

    labels.push(newData.label); // Добавление новой метки в конец
    values.push(newData.value); // Добавление нового значения в конец

    chart.update(); // Обновление графика
}



//setInterval(async () => {
//  const res = await fetch(`/get_snapshot/${simulation_id}/`);
//  console.log(res);
//}, 2000);

setInterval(() => {
  axios.get(`/get_snapshot/${simulation_id}/`)
  .then(function (response) {
    shiftChartData(response.data);
  })
}, 2000);

