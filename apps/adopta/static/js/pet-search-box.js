var apiKey = '';
$.each($('script'), function(id, val){
    var tmp_src = String($(this).attr('src'));
    var qs_index = tmp_src.indexOf('?');
    if(tmp_src.indexOf('pet-search-box.js') >= 0 && qs_index >= 0)
    {
        var params_raw = tmp_src.substr(qs_index + 1).split('&');
        apiKey = params_raw[0].split('key=')[1];
    }
});
$('#search-box').on('input',
function (e)
{
    $("#dropdown-search-box").empty();
    if (e.target.value != ''){
       $.get('/api/mascotas/', {'q': e.target.value, 'key': apiKey})
        .done(
            function(data, status)
            {
                var list = $("#dropdown-search-box").append('<ul></ul>').find('ul');
                var array = jQuery.parseJSON(data);
                console.log(array.length + " pets found");
                if (array.length == 0)
                {
                    var a = '<a><span>No hay resultados para su búsqueda</span></a>';
                    var e = '<li class="search-hidden-menu-item">' + a + '</li>';
                    list.append(e);
                }
                for (i = 0; i < array.length; i++)
                {
                    var id = array[i].id;
                    var name = array[i].name;
                    var slug = array[i].slug;
                    var img = array[i].images[0].thumbnail;

                    var thumb = '<img src="' + img +
                                '" alt="' + name + '">';
                    var a = '<a href="/mascotas/' + id + "/" +
                            slug + '">' + thumb + '<span>' +
                            name + "</span></a>";
                    var e = '<li class="search-hidden-menu-item">' + a + '</li>';
                    list.append(e);
                }
                $('#dropdown-search-box').css('visibility', 'visible');
            }
        )
    }
    else
    {
        $('#dropdown-search-box').css('visibility', 'hidden');
    }
});

$('#search-box').on('blur',
    function (e)
    {
        $('#dropdown-search-box').css('visibility', 'hidden');
    }
);

$('#search-box').on('focus',
    function (e)
    {
        if (e.target.value != '')
        {
            $('#dropdown-search-box').css('visibility', 'visible');
        }
    }
);

function getImage(id)
{
    var i;
    $.getJSON("/api/mascotas/imagenes/", {'q': id},
              function(json) {i = json[0].fields.image});
    return i;
}

