const DATA_COUNT = 7;
const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

const data = {
  labels: ['test', 'shit', 'anus'],
  datasets: [
    {
      label: 'Dataset 1',
      data: [1, 2, 1],
      fill: false,
      borderColor: 'rgba(255, 99, 132, 0.2)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
    },
        {
      label: 'Dataset 2',
      data: [2, 0, 3],
      fill: false,
      borderColor: 'rgba(255, 99, 132, 0.2)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
    }
  ]
};

const config = {
  type: 'line',
  data: data,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'left',
      },
      title: {
        display: true,
        text: 'Chart.js Line Chart'
      }
    }
  },
};