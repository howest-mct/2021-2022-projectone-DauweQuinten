

// #region ***  DOM references                           ***********

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

// #endregion



// #region ***  Callback-Visualisation - show___         ***********

const showDistance = function(payload){
  console.log(payload)
  const htmlDistance = document.querySelector('.js-distance')
  const distance = payload.value
  htmlDistance.innerHTML = `${distance} mm`
}
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
// #endregion

// #region ***  Event Listeners - listenTo___            ***********

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_ultrasonic_data", function(payload){
    showDistance(payload)
  })
};

// #endregion


// #region ***  Init / DOMContentLoaded                  ***********

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToSocket();
});


// #endregion







