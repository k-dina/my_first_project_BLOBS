var ctx = document.getElementById('realtimeChart').getContext('2d');
var step = last_step;
var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Array(10).fill(''), // Начальное заполнение пустыми метками
        datasets: [{
            label: 'Blobs population',
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

    if (!labels.includes(newData.label)) {

    labels.shift(); // Удаление первой метки
    values.shift(); // Удаление первого значения

    labels.push(newData.label); // Добавление новой метки в конец
    values.push(newData.value); // Добавление нового значения в конец

    chart.update(); // Обновление графика
}
}

let  currentTaskId = task_id;
console.log(task_id);
let simulationStopped = true;

setInterval(() => {
  axios.get(`/get_snapshots/${simulation_id}/${step}/`)
  .then(function (response) {
    console.log(response);
    const newSnapshots = response.data;
    const newSnapshotLabels = Object.keys(newSnapshots)
    step = Number(step) + newSnapshotLabels.length;
    if (!(step % 100)) {
        axios.get(`/simulation_status/${currentTaskId}/`)
        .then(function (response) {
            console.log(response)
            simulationStopped = response.data['task_is_ready'];

            if (simulationStopped) {

                axios.get(`/resume_simulation/${simulation_id}/${step}/`)
                .then(function (response) {
                currentTaskId = response.data['new_task_id'];
                console.log(currentTaskId);
                });

                }
        });

        }
    newSnapshotLabels.forEach(label => {
        shiftChartData({ label: label, value: newSnapshots[label] });
        })
  })
}, 500);




