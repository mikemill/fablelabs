$(document).ready(function(){
    $('#search-form').submit(function() {
        var terms = $('#terms').val();
        $.getJSON('/api/search?browser' + terms, function(data) {
            var table = $('#search-results');
            table.children().remove();

            if (data.files.length > 0) {
                $.each(data.files, function(index, file) {
                    var download_link = $('<a>').attr('href', '/api/get/' + file.id);
                    var row = $('<tr>')
                        .append($('<td>').append(download_link.clone().text(file.name)))
                        .append($('<td>').append(download_link.clone().text(file.file_name)));

                    table.append(row);

                });
            }
            else
            {
                $('<tr>')
                    .append($('<td colspan="2">').text('No matches found'))
                    .appendTo(table);
            }
        });
        return false;
    });
});
