var screenSize = $(window).width();
var messages = document.getElementById('chat-messages');
messages.scrollTop = messages.scrollHeight;
var c = document.getElementById('chat-panel');
var smallScreen = screenSize < 500;
var chatOpen = !smallScreen;
document.getElementById('chat-form').style.visibility = "hidden";
var currentChatId = -1;
var salt = '';

if (chatOpen)
    document.getElementById('chat-header-btn').className = 'fa fa-chevron-left';

$('#input-message').on('blur',
    function (e)
    {
        if (smallScreen)
        {
            $('#messages-panel').css('height', '100%');
            messages.scrollTop = messages.scrollHeight;
        }
    }
);

$('#input-message').on('focus',
    function (e)
    {
        if (smallScreen)
        {
            $('#messages-panel').css('height', '60%');
            messages.scrollTop = messages.scrollHeight;
        }
    }
);

$('#chat-form').submit(function( event ) {
  sendMessage();
  event.preventDefault();
});

$('#chat-panel').find('li').click(function( event ) {
    $('#chat-panel').find('li').removeClass();
    var target = $(event.currentTarget);
    target[0].className = 'active';
    document.getElementById('chat-form').style.visibility = "visible";
    var list = $("#chat-messages");
    list.empty();
    currentChatId = target[0].id;
    console.log("Chat ID: " + currentChatId);
    getChat();
    if (smallScreen)
        chatPanelAction();
});


function chatPanelAction()
{
    screenSize = $(window).width();
    smallScreen = screenSize < 500;
    if (chatOpen)
    {
        c.style.width = "0px";
        c.style.visibility = 'hidden';
        document.getElementById('chat-messages').style.visibility = "visible";
        document.getElementById('chat-header-btn').className = 'fa fa-bars';
        chatOpen = false;
    }
    else
    {
        c.style.width = "400px";
        c.style.visibility = 'visible';
        if (smallScreen)
            document.getElementById('chat-messages').style.visibility = "hidden";
        document.getElementById('chat-header-btn').className = 'fa fa-chevron-left';
        chatOpen = true;
    }
}

function sendMessage()
{
    var message = $("#input-message")[0].value;
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log("Sending message...");
    var encrypted = encrypt(message, salt);
    console.log(encrypted);
    $.post("/api/chat/" + currentChatId +"/enviar/", {'content': message, 'csrfmiddlewaretoken': csrf})
          .done(function() {
            appendMessage(message, true, myUser, convertDate(new Date()));
          })
          .fail(function() {
            alert( "error" );
          });
}

function getMessages()
{
    var list = $("#chat-messages");
    list.empty();
    var chatId = currentChatId;
    $.get('/api/chat/' + chatId + "/recibir/")
    .done(
        function(data, status)
        {
            var array = jQuery.parseJSON(data);
            if (array.length == 0)
            {
                console.log('No hay mensajes para esta conversación');
            }
            for (i = 0; i < array.length; i++)
            {
                var read = array[i].read;
                var content = array[i].content;
                var when = array[i].when;
                var mine = array[i].mine;
                var user = array[i].user;
                var message = content;
                console.log(user);
                appendMessage(message, mine, user, when);
            }
            $('#dropdown-search-box').css('visibility', 'visible');
        }
    );
}

function appendMessage(message, mine, user, when)
{
    var list = $("#chat-messages");
    user = '<h5>' + user + '<span>' + when + '</span></h5>';

    var e = "";
    if (mine)
        e = '<li class="message mine">' + user + message + '</li>';
    else
        e = '<li class="message yours">' + user + message + '</li>';
    list.append(e);
    messages.scrollTop = messages.scrollHeight;
    $("#input-message")[0].value = "";
}

function getChat()
{
    $.get('/api/chat/' + currentChatId)
    .done(
        function(data, status)
        {
            var array = jQuery.parseJSON(data);
            if (array.length == 0)
            {
                console.log('Error')
            }
            for (i = 0; i < array.length; i++)
            {
                salt = array[i].fields.salt;
                console.log(salt);
            }
        }
    )
    setTimeout(getMessages, 200);
}

function encrypt(message, salt)
{
    return CryptoJS.AES.encrypt(message, salt).toString();
}

function decrypt(message, salt)
{
    return CryptoJS.AES.decrypt(message, salt).toString(CryptoJS.enc.Utf8);
}

function convertDate(inputFormat) {
    function pad(s) { return (s < 10) ? '0' + s : s; }
    var d = new Date(inputFormat);
    return [pad(d.getHours()), pad(d.getMinutes())].join(':');
}

