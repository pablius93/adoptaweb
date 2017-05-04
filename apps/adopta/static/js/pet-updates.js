console.log(currentPet);
$('#new-pet-update-form').submit(function(event) {
    sendUpdate();
    event.preventDefault();
});

function sendUpdate()
{
    var message = $("#update-content").val();
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log("Sending update...");
    $.post("/api/mascota/" + currentPet +"/nueva-actualizacion/",
           {'content': message, 'csrfmiddlewaretoken': csrf})
           .done(function() {
               appendMessage(message);
           })
           .fail(function() {
               alert( "error" );
           });
}

function appendMessage(message)
{
    var username = $("#username").text();
    var date = new Date();
    var a = "<article class='pet-update'><a><h4><i class='fa fa-user-circle'></i>"+username+"</h4></a><h6>" + convertDate(date) + "</h6><p>" + message + "</p></article>";
    $("#pet-info-update-posts").prepend(a);
}

function convertDate(inputFormat) {
    function pad(s) { return (s < 10) ? '0' + s : s; }
    var d = new Date(inputFormat);
    return [pad(d.getDate()), pad(d.getMonth()+1), d.getFullYear()].join('/');
}
