var refreshInterval = 15; //Refresh data interval

//Retrieve temp data from API
function getPulse(device) {
  $.getJSON('api/pulse/' + device, {
    format: "json"
  }).done(function(data){
    console.log(data);
    $.each(data, function(i, item) {
      console.log(item.fields.pulse_bpm);
      $("#" + device).empty().append(item.fields.pulse_bpm + '&#8457;');   // .empty() removes old data before appending new data
    })
  })
}



//Retrieve data as soon as the page loads

getPulse("tee");

//Refresh data every 15 seconds
setInterval( function() {
  getPulse("tee");

}, refreshInterval * 1000);
