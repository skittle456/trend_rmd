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
    if ($(window).width() < 690) {
        console.log('moblie');
        return $('#vert-menu').hide();
    }
    $('.follow-btn').click(function(){
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        if ($(this).attr("name") == "unfollow"){
        console.log('following');
        var request = $.ajax({
            url: "/apis/follow/"+$(this).attr("id"),
            method: "GET",
        }).done(function(){
            //$('.fa-map-pin').css("color", "red");
            $('.follow-btn').css("color", "white");
            $('.follow-btn').css("background-color", "#FFA300");
            $('.follow-btn').attr("name","followed")
            $('.follow-btn').text("Unfollow");
            //document.location.reload(true)
        })
        .fail(function() {
            $('#login-modal').modal();
        });
    }
    else if ($(this).attr("name") == "followed"){
        console.log('unfollowing')
        var request = $.ajax({
            url: "/apis/follow/"+$(this).attr("id"),
            type: 'DELETE',
        }).done(function(){
            // $('.fa-map-pin').css("color", "red");
            $('.follow-btn').css("color", "#FFA300");
            $('.follow-btn').css("background-color", "white");
            $('.follow-btn').attr("name","unfollow");
            $('.follow-btn').text("Follow");
            //document.location.reload(true)
        })
        .fail(function() {
            $('#login-modal').modal();
        });
    }
    });
    $('.pin-item').click(function(){
        if ($(this).attr("name") == "unpin"){
            console.log('pinning');
            var request = $.ajax({
                url: "/apis/pin/"+$(this).attr("id"),
                method: "GET",
            }).done(function(){
                //$('.fa-map-pin').css("color", "red");
                $('.nav-item.pin-item').css("color", "white");
                $('.nav-item.pin-item').css("background-color", "#f9a11d");
                $('.nav-item.pin-item').css("border", "1px solid #f9a11d");
                $('.nav-item.pin-item').attr("name","pinned")
                $('#pin-text').text("Unpin this post");
                $(".pin-label").attr("src","/static/images/pin_orange.png");
            })
            .fail(function() {
                $('#login-modal').modal();
            });
        }else if($(this).attr("name") == "pinned"){
            console.log('unpinning');
            var request = $.ajax({
                url: "/apis/pin/"+$(this).attr("id"),
                method: "DELETE",
            }).done(function(){
                //$('.fa-map-pin').css("color", "red");
                $('.nav-item.pin-item').css("background-color", "grey");
                $('.nav-item.pin-item').css("border", "1px solid white");
                $('.nav-item.pin-item').attr("name","unpin")
                $('#pin-text').text("Pin this post");
                $(".pin-label").attr("src","/static/images/pin_white.png");
            })
            .fail(function() {
                $('#login-modal').modal();
            });
        }
    });
    $('.like-btn').click(function(){
        if ($(this).attr("name") == "unlike"){
            console.log('liking');
            var request = $.ajax({
                url: "/apis/like/"+$(this).attr("id"),
                method: "GET",
            }).done(function(){
                //$('.fa-map-pin').css("color", "red");
                $('.like-btn').css("color", "#f9a11d");
                $('.like-btn').css("background-color", "white");
                $('.like-btn').attr("name","liked")
                $('.like-label').css("color","#f9a11d");
                $('.like-label').css("background-color", "transparent");
                var count = parseInt($('.nav-item.like-num').text());
                count=count+1;
                $('.like-num').text(count);
            })
            .fail(function() {
                $('#login-modal').modal();
            });
        }else if($(this).attr("name") == "liked"){
            console.log('unliking');
            var request = $.ajax({
                url: "/apis/like/"+$(this).attr("id"),
                method: "DELETE",
            }).done(function(){
                //$('.fa-map-pin').css("color", "red");
                $('.like-btn').css("color", "white");
                $('.like-btn').css("background-color", "lightgrey");
                $('.like-btn').attr("name","unlike");
                $('.like-label').css("color","lightgrey");
                $('.like-label').css("background-color", "transparent");
                var count = parseInt($('.nav-item.like-num').text());
                count=count-1;
                $('.like-num').text(count);
            })
            .fail(function() {
                $('#login-modal').modal();
            });
        }
    });
    $('div.back').click(function(){
        console.log('back clicked');
        window.history.back;
    });
    $('.new-reply').click(function(){
        element = $(this).data('comment');
        $( "#new-reply-" + element ).toggle();
        $( "#new-reply-" + element ).focus();

    });
    $('.new-comment').keypress(function(e,data){
        if (e.keyCode == 13){
            message = $(this).val();
            if (message !== ''){
                insource = $(this).data('insource');
                userID = $(this).data('uid');
                name = $(this).data('uname');;
                head = $(this).data('head') === 'null' ? null : $(this).data('head');
                var request = $.ajax({
                    url: "/apis/comment_list/",
                    method: "POST",
                    contentType: "application/json",
                    dataType: "json",
                    data: JSON.stringify({
                        "message": message,
                        "user": userID,
                        "insource": insource,
                        "reply_to": head
                    }),
                }).done(function(){
                    var element = head === null ? $('#comment-container') : $('#reply-block-'+head);
                    element.append(
                    '<div class="row'+ (head === null ? '' : ' comment-reply') + '">' +
                        '<div class="col-xs-3 comment-img">' +
                            '<i class="fa fa-user-circle comment-img"></i>' +
                        '</div>' +
                        '<div class="col-xs comment-content">' +
                            '<a class="comment-head responsive-text">' + name +' </a>' +
                            '<p class="comment-text responsive-text"> ' + message + '</p>' +
                            '<p class="comment-text comment-time responsive-text"> Just now </p>' +
                        '</div>' +
                    '</div>');
                })
                .fail(function() {
                    $('#login-modal').modal();
                });
                $(this).val('');
            }
            if(e.preventDefault) event.preventDefault(); 
            return false;
        }
    });
});



