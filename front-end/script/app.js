// #region ***  DOM references                           ***********

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
let fillBtn;
let chart;
let htmlStats;

// #endregion

// #region *** Hulpfuncties

const clearClassList = function (el) {
  el.classList.remove('c-fill-btn--wait');
  el.classList.remove('c-fill-btn--active');
};

const setFillBtn = function (state) {
  if (state == 0) {
    fillBtn.innerHTML = `vullen
    <svg
      class="c-fill-btn__svg"
      xmlns="http://www.w3.org/2000/svg"
      enable-background="new 0 0 24 24"
      height="24px"
      viewBox="0 0 24 24"
      width="24px"
      fill="#005780"
    >
      <rect fill="none" height="24" width="24" />
      <path
        d="M12,2c-5.33,4.55-8,8.48-8,11.8c0,4.98,3.8,8.2,8,8.2s8-3.22,8-8.2C20,10.48,17.33,6.55,12,2z M12,20c-3.35,0-6-2.57-6-6.2 c0-2.34,1.95-5.44,6-9.14c4.05,3.7,6,6.79,6,9.14C18,17.43,15.35,20,12,20z M7.83,14c0.37,0,0.67,0.26,0.74,0.62 c0.41,2.22,2.28,2.98,3.64,2.87c0.43-0.02,0.79,0.32,0.79,0.75c0,0.4-0.32,0.73-0.72,0.75c-2.13,0.13-4.62-1.09-5.19-4.12 C7.01,14.42,7.37,14,7.83,14z"
      />
    </svg>`;
  } else {
    fillBtn.innerHTML = `bezig met vullen
    <svg
      class="c-fill-btn__svg"
      xmlns="http://www.w3.org/2000/svg"
      enable-background="new 0 0 24 24"
      height="24px"
      viewBox="0 0 24 24"
      width="24px"
      fill="#005780"
    >
      <rect fill="none" height="24" width="24" />
      <path
        d="M12,2c-5.33,4.55-8,8.48-8,11.8c0,4.98,3.8,8.2,8,8.2s8-3.22,8-8.2C20,10.48,17.33,6.55,12,2z M12,20c-3.35,0-6-2.57-6-6.2 c0-2.34,1.95-5.44,6-9.14c4.05,3.7,6,6.79,6,9.14C18,17.43,15.35,20,12,20z M7.83,14c0.37,0,0.67,0.26,0.74,0.62 c0.41,2.22,2.28,2.98,3.64,2.87c0.43-0.02,0.79,0.32,0.79,0.75c0,0.4-0.32,0.73-0.72,0.75c-2.13,0.13-4.62-1.09-5.19-4.12 C7.01,14.42,7.37,14,7.83,14z"
      />
    </svg>`;
  }
};

// #endregion

// #region ***  Callback-Visualisation - show___         ***********

const showCurrentVolume = function (payload) {
  const currentVolume = payload.value;
  const maxVolume = 5.8;
  const percentage = (currentVolume / maxVolume) * 100;
  chart.updateSeries([percentage]);
};

const drawChart = function () {
  const maxVolume = 5.8; // hardcoded -> kan eventueel later uit de database gehaald worden.

  var options = {
    series: [0],
    chart: {
      height: 350,
      type: 'radialBar',
      toolbar: {
        show: true,
      },
    },
    plotOptions: {
      radialBar: {
        startAngle: -135,
        endAngle: 225,
        hollow: {
          margin: 0,
          size: '70%',
          background: '#fff',
          image: undefined,
          imageOffsetX: 0,
          imageOffsetY: 0,
          position: 'front',
          dropShadow: {
            enabled: true,
            top: 3,
            left: 0,
            blur: 4,
            opacity: 0.24,
          },
        },
        track: {
          background: '#fff',
          strokeWidth: '67%',
          margin: 0, // margin is in pixels
          dropShadow: {
            enabled: true,
            top: -3,
            left: 0,
            blur: 4,
            opacity: 0.35,
          },
        },

        dataLabels: {
          show: true,
          name: {
            offsetY: -10,
            show: true,
            color: '#888',
            fontSize: '17px',
          },
          value: {
            formatter: function (val) {
              // return parseInt(val);
              return parseInt(val * maxVolume) / 100;
            },
            color: '#111',
            fontSize: '36px',
            show: true,
          },
        },
      },
    },
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'dark',
        type: 'horizontal',
        shadeIntensity: 0.5,
        gradientToColors: ['#ABE5A1'],
        inverseColors: true,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 100],
      },
    },
    stroke: {
      lineCap: 'round',
    },
    labels: ['liter'],
  };

  chart = new ApexCharts(document.querySelector('.js-level-chart'), options);
  chart.render();
};

const drawStats = function () {
  var options = {
    series: [
      {
        name: 'Volume',
        data: [1, 3, 2, 5, 4, 2, 1, 3, 2],
      },
    ],
    chart: {
      height: 350,
      type: 'area',
      zoom: {
        enabled: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth',
    },
    title: {
      text: 'Water volume',
      align: 'center',
    },
    xaxis: {
      categories: [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
      ],
    },
  };

  var chart = new ApexCharts(
    document.querySelector('.js-stats-chart'),
    options
  );
  chart.render();
};

// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********

// #endregion

// #region ***  Data Access - get___                     ***********
// #endregion

// #region ***  Event Listeners - listenTo___            ***********

const listenToSocket = function () {
  socket.on('connect', function () {
    console.log('verbonden met socket webserver');
  });

  socket.on('B2F_initial-valve-state', function (payload) {
    console.log('dit is de status van het ventiel:');
    console.log(payload);
    fillBtn.dataset.status = payload.state;
    clearClassList(fillBtn);

    if (fillBtn.dataset.status == 1) {
      fillBtn.classList.add('c-fill-btn--active');

      setFillBtn(1);
    }
  });

  socket.on('B2F_switched_valve', function (payload) {
    state = payload['state'];
    fillBtn.dataset.status = state;
    clearClassList(fillBtn);

    if (state == 1) {
      fillBtn.classList.add('c-fill-btn--active');
      setFillBtn(1);
    }
  });

  socket.on('B2F_ultrasonic_data', function (payload) {
    showDistance(payload);
  });

  socket.on('B2F_current_volume', function (payload) {
    showCurrentVolume(payload);
  });

  socket.on('B2F_changed_by_hardware', function (payload) {
    const newState = payload['state'];
    fillBtn.dataset.status = newState;
    clearClassList(fillBtn);

    if (newState == 1) {
      fillBtn.classList.add('c-fill-btn--active');
      setFillBtn(1);
    } else {
      setFillBtn(0);
    }
  });
};

const listenToFillBtn = function () {
  document.querySelector('.js-btn-fill').addEventListener('click', function () {
    const currentState = this.dataset.status;
    let newState;

    if (currentState == 0) {
      newState = 1;
    } else {
      newState = 0;
    }

    clearClassList(this);
    setFillBtn(0);

    if (newState == 1) {
      this.classList.add('c-fill-btn--wait');
    }

    socket.emit('F2B_switch_valve', { state: newState });
  });
};

const listenToShutdown = function () {
  const shutdownBtn = document.querySelector('.js-shutdown');
  shutdownBtn.addEventListener('click', function () {
    console.info('shutdown activated ❌');
    socket.emit('F2B_shutdown', { state: 'shutdown' });
  });
};

// #endregion

// #region ***  Init / DOMContentLoaded                  ***********

document.addEventListener('DOMContentLoaded', function () {
  console.info('DOM geladen');
  fillBtn = document.querySelector('.js-btn-fill');
  htmlStats = document.querySelector('.js-stats');

  if (fillBtn) {
    console.info('🏠');
    drawChart();
    listenToSocket();
    listenToFillBtn();
  } else if (htmlStats) {
    console.info('📊');
  }
  listenToShutdown();
  drawStats();
});

// #endregion
