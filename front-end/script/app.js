// #region ***  DOM references                           ***********

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

// #endregion

// #region ***  Callback-Visualisation - show___         ***********

const showDistance = function (payload) {
  console.info(payload);
  const htmlDistance = document.querySelector('.js-distance');
  const distance = payload.value;
  htmlDistance.innerHTML = `${distance} mm`;

  const body = JSON.stringify({
    value: distance,
    deviceid: 1,
    commentaar: 'level measurement',
  });

  const url = `http://192.168.168.169:5000/api/v1/historiek/`;

  handleData(url, callbackLevelMeasurement, null, 'POST', body);
};
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********

const callbackLevelMeasurement = function (jsonobject) {
  console.log('created');
  // console.info(jsonobject);
};

// #endregion

// #region ***  Data Access - get___                     ***********
// #endregion

// #region ***  Event Listeners - listenTo___            ***********

const listenToSocket = function () {
  socket.on('connect', function () {
    console.log('verbonden met socket webserver');
  });

  socket.on('B2F_ultrasonic_data', function (payload) {
    showDistance(payload);
  });
};

// #endregion

// #region ***  Init / DOMContentLoaded                  ***********

document.addEventListener('DOMContentLoaded', function () {
  console.info('DOM geladen');
  listenToSocket();
});

// #endregion
