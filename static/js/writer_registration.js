$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
});
$(document).ready(function() {
    $('.table-selector').click(function(){
        $('.table-selector').removeClass('table-selector-selected');
        $(this).addClass('table-selector-selected');
        $('.register-table-list').hide();
    });
    $('#pending-table-selector').click(function(){
        $('#pending-table').show();
    });
    $('#approved-table-selector').click(function(){
        $('#approved-table').show();
    });
    $('#rejected-table-selector').click(function(){
        $('#rejected-table').show();
    });
    // When accept
    $('.btn-accept').click(function(){
        const id = $(this).data('id');
        const row = $(this).data('row');
        const name = $(this).data('name');
        var request = $.ajax({
            url: "/apis/writer_registration_detail/" + id,
            method: "PATCH",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "status": "approved"
            }),
        }).done(function(){
            // Move to approved
            $('#'+row).remove();
            $('#approved-table-body').append(
                '<tr id="approved-'+id+'">' +
                '<th scope="row"> ' + name + '</th>' +
                '<td>' +
                    '<button type="button" class="btn-status btn-danger btn-reject" ' +
                    'data-id="' + id + '" data-row="approved-' + id + '"' +
                    'data-name="' + name + '">' +
                        'Revoke' +
                    '</button>' +
                '</td>' +
            '</tr>'
            );
        })
    });
    // When Reject
    $('.btn-reject').click(function(){
        const id = $(this).data('id');
        const row = $(this).data('row');
        const name = $(this).data('name');
        var request = $.ajax({
            url: "/apis/writer_registration_detail/" + id,
            method: "PATCH",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "status": "declined"
            }),
        }).done(function(){
            // Move to declined
            $('#'+row).remove();
            $('#rejected-table-body').append(
                '<tr id="rejected-'+id+'">' +
                '<th scope="row"> ' + name + '</th>' +
                '<td>' +
                    '<button type="button" class="btn-status btn-success btn-approve" ' +
                    'data-id="' + id + '" data-row="rejected-' + id + '"' +
                    'data-name="' + name + '">' +
                        'Approve' +
                    '</button>' +
                '</td>' +
            '</tr>'
            );
            
        })        
    });
    $('#pending-table-selector').addClass('table-selector-selected');
    $('#approved-table').hide();
    $('#rejected-table').hide();
});


