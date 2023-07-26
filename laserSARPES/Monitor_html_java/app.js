window.onload = Main;

const base_url = "https://api.thingspeak.com/channels/2213864/feeds.json";
const api_key = "";

let app;
let chart1;
let chart2;
let chart3;
let chart4;
let chart5;

function Main() {
  app = new Vue({
    el: "#app",
    data: {
      createdAt: [],
      field1: [],
      field2: [],
      field3: [],
      field4: [],
      field5: [],
      field6: [],
      field7: [],
      latestValues: {
        field1: '',
        field2: '',
        field3: '',
        field4: '',
        field5: '',
        field6: '',
        field7: ''
      }
    },
    mounted: function () {
      updateInitialData();
      setInterval(updateLatestData, 5000); // 5秒ごとに最新のデータを更新
    }
  });
}

async function updateInitialData() {
  const result_num = 600; // 最初に表示するデータ点数

  let url = `${base_url}?api_key=${api_key}&timezone=Asia/Tokyo&results=${result_num}`;

  try {
    const response = await fetch(url, { method: 'GET', cache: 'no-store' });
    const res = await response.json();

    let createdAt = [];
    let field1 = [];
    let field2 = [];
    let field3 = [];
    let field4 = [];
    let field5 = [];
    let field6 = [];
    let field7 = [];

    res.feeds.forEach(elm => {
      createdAt.push(elm.created_at);
      field1.push(parseFloat(elm.field1));
      field2.push(parseFloat(elm.field2));
      field3.push(parseFloat(elm.field3));
      field4.push(parseFloat(elm.field4));
      field5.push(parseFloat(elm.field5));
      field6.push(parseFloat(elm.field6));
      field7.push(parseFloat(elm.field7));
    });

    app.createdAt = createdAt;
    app.field1 = field1;
    app.field2 = field2;
    app.field3 = field3;
    app.field4 = field4;
    app.field5 = field5;
    app.field6 = field6;
    app.field7 = field7;

    updateCharts();
  } catch (error) {
    console.error("データの取得エラー:", error);
  }
}

async function updateLatestData() {
  const latest_num = 1; // 最新のデータ点数

  let url = `${base_url}?api_key=${api_key}&timezone=Asia/Tokyo&results=${latest_num}`;

  try {
    const response = await fetch(url, { method: 'GET', cache: 'no-store' });
    const res = await response.json();

    const latestData = res.feeds[0];

    app.latestValues.createdAt = formatDateTime(latestData.created_at);
    app.latestValues.field1 = parseFloat(latestData.field1);
    app.latestValues.field2 = parseFloat(latestData.field2);
    app.latestValues.field3 = parseFloat(latestData.field3);
    app.latestValues.field4 = parseFloat(latestData.field4);
    app.latestValues.field5 = parseFloat(latestData.field5);
    app.latestValues.field6 = parseFloat(latestData.field6);
    app.latestValues.field7 = parseFloat(latestData.field7);

    // データを追加してグラフを更新
    app.createdAt.push(latestData.created_at);
    app.field1.push(parseFloat(latestData.field1));
    app.field2.push(parseFloat(latestData.field2));
    app.field3.push(parseFloat(latestData.field3));
    app.field4.push(parseFloat(latestData.field4));
    app.field5.push(parseFloat(latestData.field5));
    app.field6.push(parseFloat(latestData.field6));
    app.field7.push(parseFloat(latestData.field7));

    if (app.createdAt.length > 500) {
      // グラフの表示点数が500を超えた場合、古いデータを削除
      app.createdAt.shift();
      app.field1.shift();
      app.field2.shift();
      app.field3.shift();
      app.field4.shift();
      app.field5.shift();
      app.field6.shift();
      app.field7.shift();
    }

    updateCharts();
  } catch (error) {
    console.error("データの取得エラー:", error);
  }
}

function updateCharts() {
  // グラフの更新処理

  // ...
}

function formatTicks(value) {
  // ...
}

function formatDateTime(date) {
  // ...
}

function updateCharts() {
  let labels = app.createdAt.map((date, index) => {
    const dateTime = new Date(date);
    const formattedDate = index === 0 ? `${dateTime.getFullYear()}-${("0" + (dateTime.getMonth() + 1)).slice(-2)}-${(
      "0" + dateTime.getDate()
    ).slice(-2)}` : '';
    const formattedTime = `${("0" + dateTime.getHours()).slice(-2)}:${("0" + dateTime.getMinutes()).slice(-2)}:${("0" + dateTime.getSeconds()).slice(-2)}`;
    return `${formattedDate} ${formattedTime}`;
  });

  let field1Data = app.field1;
  let field2Data = app.field2;
  let field3Data = app.field3;
  let field4Data = app.field4;
  let field5Data = app.field5;
  let field6Data = app.field6;
  let field7Data = app.field7;
  const maxDataPoints = 600;
  if (field1Data.length > maxDataPoints) {
    labels = labels.slice(-maxDataPoints);
    field1Data = field1Data.slice(-maxDataPoints);
    field2Data = field2Data.slice(-maxDataPoints);
    field3Data = field3Data.slice(-maxDataPoints);
    field4Data = field4Data.slice(-maxDataPoints);
    field5Data = field5Data.slice(-maxDataPoints);
    field6Data = field6Data.slice(-maxDataPoints);
    field7Data = field7Data.slice(-maxDataPoints);
  }

  if (chart1) {
    chart1.data.labels = labels;
    chart1.data.datasets[0].data = field1Data;
    chart1.update();
  } else {
    let ctx1 = document.getElementById('chart1').getContext('2d');
    chart1 = new Chart(ctx1, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Main pressure',
          data: field1Data,
          borderColor: 'red',
          fill: false
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Date and Time'
            }
          },
          y: {
            position: 'left',
            type: 'linear',
            display: true,
            title: {
              display: true,
              text: 'Main (Pa)',
              color: 'red'
            },
            ticks: {
              color: 'red',
              callback: formatTicks
            },
            grid: {
              drawOnChartArea: false
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Main pressure'
          },
          legend: {
            labels: {
              fontColor: 'black'
            }
          }
        }
      }
    });
  }

  if (chart2) {
    chart2.data.labels = labels;
    chart2.data.datasets[0].data = field2Data;
    chart2.data.datasets[1].data = field3Data;
    chart2.update();
  } else {
    let ctx2 = document.getElementById('chart2').getContext('2d');
    chart2 = new Chart(ctx2, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Prep (Pa)',
          data: field2Data,
          borderColor: 'blue',
          fill: false
        },
        {
          label: 'Vprep',
          data: field3Data,
          borderColor: 'green',
          fill: false
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Date and Time'
            }
          },
          y: {
            position: 'left',
            type: 'linear',
            display: true,
            title: {
              display: true,
              text: 'Prep, Vprep (Pa)',
              color: 'blue'
            },
            ticks: {
              color: 'blue',
              callback: formatTicks
            },
            grid: {
              drawOnChartArea: false
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Prep, Vprep pressure'
          },
          legend: {
            labels: {
              fontColor: 'black'
            }
          }
        }
      }
    });
  }

  if (chart3) {
    chart3.data.labels = labels;
    chart3.data.datasets[0].data = field4Data;
    chart3.update();
  } else {
    let ctx3 = document.getElementById('chart3').getContext('2d');
    chart3 = new Chart(ctx3, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Loadlock pressure',
          data: field4Data,
          borderColor: 'black',
          fill: false
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Date and Time'
            }
          },
          y: {
            position: 'left',
            type: 'linear',
            display: true,
            title: {
              display: true,
              text: 'LL pressure (Pa)',
              color: 'black'
            },
            ticks: {
              color: 'black',
              callback: formatTicks
            },
            grid: {
              drawOnChartArea: false
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'LoadLock pressure'
          },
          legend: {
            labels: {
              fontColor: 'black'
            }
          }
        }
      }
    });
  }

  if (chart4) {
    chart4.data.labels = labels;
    chart4.data.datasets[0].data = field5Data;
    chart4.data.datasets[1].data = field6Data;
    chart4.update();
  } else {
    let ctx4 = document.getElementById('chart4').getContext('2d');
    chart4 = new Chart(ctx4, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Cryo',
          data: field4Data,
          borderColor: 'red',
          fill: false
        },
        {
          label: 'Sample',
          data: field5Data,
          borderColor: 'blue',
          fill: false
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Date and Time'
            }
          },
          y: {
            position: 'left',
            type: 'linear',
            display: true,
            title: {
              display: true,
              text: 'Temperature (K)',
              color: 'black'
            },
            ticks: {
              color: 'black'
            },
            grid: {
              drawOnChartArea: false
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Temperature'
          },
          legend: {
            labels: {
              fontColor: 'black'
            },
            display: true,
            boxWidth: 0
          }
        }
      }
    });
  }

  if (chart5) {
    chart5.data.labels = labels;
    chart5.data.datasets[0].data = field7Data;
    chart5.update();
  } else {
    let ctx5 = document.getElementById('chart5').getContext('2d');
    chart5 = new Chart(ctx5, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Pulse width',
          data: field7Data,
          borderColor: 'black',
          fill: false
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Date and Time'
            }
          },
          y: {
            position: 'left',
            type: 'linear',
            display: true,
            title: {
              display: true,
              text: 'Pulse width (ps)',
              color: 'black'
            },
            grid: {
              drawOnChartArea: false
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Pulse width'
          },
          legend: {
            labels: {
              fontColor: 'black'
            }
          }
        }
      }
    });
  }

  

  const latestValuesDiv = document.getElementById('latestValues');
  latestValuesDiv.innerHTML = `
    <p><b>${app.latestValues.createdAt}</b></p>
	<p><font color="red"><b>Main: ${app.latestValues.field1} Pa</b></font> <font color="blue"><b>Prep: ${app.latestValues.field2} Pa</b></font> <font color="green"><b>Vprep: ${app.latestValues.field3} Pa</b></font></p>
  <p><font color="black"><b>LoadLock: ${app.latestValues.field4} Pa</b></font></p>
	<p><font color="red"><b>Cryo: ${app.latestValues.field5} K</b></font>, <font color="blue"><b>Sample: ${app.latestValues.field6} K</b></font></p>
  <p><font color="black"><b>Pulse: ${app.latestValues.field7} ps</b></font></p>
  `;
}

function formatTicks(value) {
  if (Math.abs(value) >= 1e-3) {
    return value.toExponential(1);
  } else {
    return value.toExponential(2);
  }
}

function formatDateTime(date) {
  const dateTime = new Date(date);
  const formattedDate = `${dateTime.getFullYear()}-${("0" + (dateTime.getMonth() + 1)).slice(-2)}-${("0" + dateTime.getDate()).slice(-2)}`;
  const formattedTime = `${("0" + dateTime.getHours()).slice(-2)}:${("0" + dateTime.getMinutes()).slice(-2)}:${("0" + dateTime.getSeconds()).slice(-2)}`;
  return `${formattedDate} ${formattedTime}`;
}