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

function reload_elements(){
    pathName = window.location.pathname;
    var element_selected = $('.on-selected');
    element_selected.removeClass('on-selected');
    var element_tagged = $(".on-tagged");
    element_tagged.removeClass("on-tagged");
    var provider_path = $('.pro_name').attr('id').toLowerCase();
    //use as bug should be fixed later
    if (location.pathname == "/provider/"+provider_path) {
        $('#feed').addClass('on-selected');
    }
    // else {
    //     $('#trending-container').hide();
    // }
    if (pathName.search("/provider/"+provider_path+"/category/") != -1){
      let categoryName = pathName.substring(pathName.lastIndexOf('/') + 1);
      $( "#"+categoryName ).addClass( "on-selected" );
    }
    else if (pathName.search("/provider/"+provider_path+"/tag/") != -1){
        let tagName = pathName.substring(pathName.lastIndexOf('/') + 1);
        // $('#feed').addClass('on-selected');
        $("#"+tagName).addClass( "on-tagged");
        // $("#tag-"+tagName).prependTo(".tag-bar");
        $(".nav-tag").animate({ scrollLeft: 0 }, "slow");
        return false;
      }
    else if (pathName.search("/provider/"+provider_path) != -1){
        $('.nav-category').addClass('fixed');
        $('.nav-tag').addClass('tag-fixed');
        $('.nav-category').addClass('nav-ontop-category');
        $('.nav-tag').addClass('nav-ontop-tag');
    }
      if($('.searchbar').val() != ""){
        var element_selected = $('.on-selected');
        element_selected.removeClass('on-selected');
        var element_tagged = $(".on-tagged");
        element_tagged.removeClass("on-tagged");
      }
}

$(document).ready(function() {
    $('.nav-category').addClass('fixed');
    $('.nav-category').addClass('nav-ontop-category');
    $('#trending-container').hide();
    $('.on-selected').removeClass('on-selected');
    //$('#tag-container').prepend($('.nav-tag'));
    $('#blog-container').prepend($('.loading'));
    $('.nav-tag').show();

    // $('input.form-control').keypress(function (e) {
    //     if (e.which == 13) {
    //         console.log('hit enter');
    //       $('#search-form').submit();
    //       return false;
    //     }
    //   });
    $('div.category-title').click(function() {
        $('.searchbar').val("")
        var category = $(this).attr('id');
        var provider_path = $('.pro_name').attr('id').toLowerCase();
        $('#blog-container').fadeOut();
        $('.loading').css("display", "block");
        var path = '/provider/'+provider_path+'/category/'+category;
        $('#blog-container').load(path, function() {
            $('.loading').css("display", "none");
            $(this).fadeIn();
          });
        history.pushState(null, null, path);
        reload_elements();
    });
    $('span.blog-tag').click(function() {
        $('.searchbar').val("")
        var tag_path = $(this).attr('id');
        var provider_path = $('.pro_name').attr('id').toLowerCase();
        $('#blog-container').fadeOut();
        $('.loading').css("display", "block");
        var path = '/provider/'+provider_path+'/tag/'+tag_path;
        $('#blog-container').load(path, function() {
            $('.loading').css("display", "none");
            $(this).fadeIn();
          });
        history.pushState(null, null, path);
        reload_elements();
    });
    $(".nav-tag").click(function(e) {
        var position = e.pageX;
        if(event.target.nodeName.toLowerCase() == 'div' ) {
            // code
            var x = $(".nav-tag").scrollLeft();
            if (position > $(window).width()/2){
                x+=180;
            }
            else if (position < $(window).width()/2){
                x-=180;
            }
            $(".nav-tag").animate({ scrollLeft: x }, "slow");
            }
    });
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
});