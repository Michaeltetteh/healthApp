function chartTemps_all(datapoints, isDisplayEnabled) {
  //Get API data
  $.getJSON('api/PulseModel/', {
    format: "json"
  }).done(function(data){
    console.log(data);
    

    var newDateArr = data.map(function(e) {
      return e.date;
    });

    var newPulseArr = data.map(function(e) {
      return e.pulse_bpm;
    });

    new_PulseChart(newDateArr, newPulseArr, "All Temperatures", isDisplayEnabled);
  });
}

function chartPulse(device, datapoints, isDisplayEnabled) {
  //had to use the absolute path
  // replace on local run 
  //$.getJSON('http://127.0.0.1:8000/api/pulse/' + device + '/' + datapoints, {
  $.getJSON('https://healthapp-prod.herokuapp.com/api/pulse/' + device + '/' + datapoints, {
  }).done(function(data){
    console.log(data);
    console.log(data.reverse());

    var newDateArr = $.map(data, function(e) {
      return new Date(e.fields.date).toLocaleString();
    });

    var newPulseArr = $.map(data, function(e) {
      console.log(e.fields.pulse_bpm)
      return e.fields.pulse_bpm;
    });

    console.log(newDateArr);
    new_PulseChart(newDateArr, newPulseArr, device, isDisplayEnabled);
  });
}

function new_PulseChart(labels, data, device, isDisplayEnabled) {
  //Create the chart
  var ctx = document.getElementById(device + "-pulse").getContext('2d');

  var pulseChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        label: "Pulse Rate",
        //backgroundColor: ['rgba(115, 134, 213, .4)']
      }]
    },
    options: {
      scales: {
        xAxes: [{
          display: isDisplayEnabled //false or true
        }]
      },
      title: {
        display: true,
        text: device,
      },
      responsive: true,
      maintainAspectRatio: false,
      responsiveAnimationDuration: 30,
    }
  });
}

function addDatapoint() {
  var oldVal = +$('#datapoints-input').val();
  var newVal = (oldVal + 1);

  $('#datapoints-input').val(newVal);
}

function subDatapoint() {
  var oldVal = +$('#datapoints-input').val();
  var newVal = (oldVal - 1);

  $('#datapoints-input').val(newVal);
}

function updateChart() {
  var device = $('#room-name').val();
  var newDatapoints = $('#datapoints-input').val();

  chartPulse(deviceValue, newDatapoints);

}
