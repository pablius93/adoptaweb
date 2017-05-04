var page = 1;
$('#load-button').on('click',
    function (e) {
        page++;
        $.get('/api/mascotas/todas/?pagina=' + page)
        .always(function() {
            $('#load-button-i').attr('class', 'fa fa-spinner fa-pulse fa-3x fa-fw');
        })
        .done(
            function(data, status)
            {
                var array = jQuery.parseJSON(data);
                if (array.length == 0)
                {
                    console.log('No more pets to show');
                    $('#load-button').hide();
                    $('#no-results').fadeIn('slow');
                }
                for (i = 0; i < array.length; i++)
                {
                    var name = array[i].name;
                    var description = array[i].description;
                    var url = array[i].url;
                    var image = array[i].images[0].image;
                    var days = array[i].days_waiting;
                    console.log(name);
                    appendPet(name, description, url, image, days);
                }
                $('#load-button-i').attr('class', 'fa fa-plus');
            }
        );
    }
);

function appendPet(name, description, url, image, days_waiting)
{
    console.log('Añadiendo a ' + name);
    var article = $('<article>', {'class': 'pet-item'});
    var a = $('<a>', {'href': url});
    var img = $('<img>', {'src': image, 'alt': name});
    var h3 = $('<h3>', {'class': 'pet-item-header'});
    var title = $('<a>', {'href': url}).append(name);
    var h6 = $('<h6>').append(days_waiting + ' días esperando hogar');
    var p = $('<p>', {'class': 'pet-item-description'}).append(description);
    var more = $('<a>', {'href': url}).append(' Ver más');

    a.append(img);
    h3.append(title);
    p.append(more);
    article.append(a);
    article.append(h3);
    article.append(title);
    article.append(h6);
    article.append(p);
    $('#pet-grid').append(article);
}
