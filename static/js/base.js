
$(document).ready(function (){
    $('.nav-brand').hide();
    $('body').click(function(evt){   
        if($(evt.target).is('.sidebar-collaspe')) {
            //event handling code
            $('#sidebar').toggleClass('active');
            $('.collapse.in').toggleClass('in');
            $('a[aria-expanded=true]').attr('aria-expanded', 'false');
            return
        }


        $('#sidebar').addClass('active')
        $('.collapse.in').addClass('in');
        $('a[aria-expanded=false]').attr('aria-expanded', 'True');
    });
    if ($(window).width() < 690) {
        //return $('.mainbar').addClass('navbar-expand-md');
        console.log('moblie');
        // $('.search-item').hide();
        $('.trending-container-md').remove();
        $('.logo-brand').remove();
        $('.nav-md').remove()
        $('.searchbar').hide();
    }
    else{
        $('.trending-container-sm').remove();
        $('.nav-sm').remove();
        $('.nav-search').remove();
        // $('.mobile-search').hide();
        // $('.search-button').hide()
        // $('#sidebar').toggleClass('active');
    }
    $('.search-btn').on('click', function(){
        if(this.id != 'show'){
            this.id = "show";
            $('.searchbar').fadeIn();
            return
        }
        this.id = "hide";
        $('.searchbar').hide();
    });
    $('.writer-checkbox').change(function() {
        $('#writer-text').attr('disabled',!this.checked)
    });
    $('.blog-tag').on('click', function() {
        $('.searchbar').val("")
        var tag_path = $(this).attr('id');
        var category_path = $('.on-selected').attr('id');
        $('#blog-container').fadeOut();
        $('.loading').css("display", "block");
        var path = '/tag/'+tag_path;
        if (location.pathname == "/tag/"+tag_path){
            return $('html,body').animate({
                scrollTop: $("#blog-container").offset().top
            }, 'slow');
        }
        else if(location.pathname == "/category/"+category_path+"/tag/"+tag_path){
            path = "/category/"+category_path;
        }
        else if(tag_path == "feed"){
            //// rewrite this function
            path="/";
        }
        if(!$('#blog-container').length){
            window.location.href = path;
        }
        $('#blog-container').load(path, function() {
            $('.loading').css("display", "none");
            $(this).fadeIn();
          });
        history.pushState(null, null, path);
        reload_elements();
        //$("html, body").animate({ scrollTop: 0 }, "slow");
        $('html,body').animate({
            scrollTop: $("#blog-container").offset().top
        }, 'slow');
    });
    var lastScrollTop = 0;
    var nav = $('.mainbar');
    var nav_category = $('.nav-category');
    var nav_tag = $('.nav-tag');
    $(window).scroll(function(event){
       var st = $(this).scrollTop();
       //console.log(st);
       if (st > lastScrollTop && st > 56){
        // downscroll code
        nav.fadeOut(10);
        if(st >= 90){
         nav_category.addClass('fixed');
         nav_tag.addClass('tag-fixed');
         nav_category.removeClass('nav-ontop-category');
         nav_tag.removeClass('nav-ontop-tag');
         $('.nav-brand').fadeIn();
        }
        else{
         nav_category.removeClass('fixed');
         nav_tag.removeClass('tag-fixed');
         nav_category.removeClass('nav-ontop-category');
         nav_tag.removeClass('nav-ontop-tag');
         $('.nav-brand').hide();
        }
    } else{
       // upscroll code
        if(st + $(window).height() < $(document).height()){
             //nav.removeClass('nav-up');
             nav.fadeIn(10);
             nav_category.addClass('fixed');
             nav_tag.addClass('tag-fixed');
            //  nav_category.addClass('nav-ontop-category');
            //  nav_tag.addClass('nav-ontop-tag');
             if(st <= 305){
                 nav_category.removeClass('fixed');
                 nav_tag.removeClass('tag-fixed');
                //  nav_category.removeClass('nav-ontop-category');
                //  nav_tag.removeClass('nav-ontop-tag');
                 $('.nav-brand').hide();
                }
     }
    }
       lastScrollTop = st;
    });
});


function post_feedback(){
    console.log($('textarea#message-text.form-control').val());
    console.log($('input#email.form-control').val());
    var request = $.ajax({
        url: "/apis/feedback_list",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "email":$('input#email.form-control').val(),
            "feedback_message":$('textarea#message-text.form-control').val()
        }),
    }).done(function(){
        $('input#email.form-control').val('');
        $('textarea#message-text.form-control').val('');
        $('button.close').click();
        alert("Thank you for feedback");
    })
    .fail(function() {
        alert("fail")
    });
}


function login(){
    console.log('logging in');
    var request = $.ajax({
        url: "/apis/login",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "username":$('#login-username').val(),
            "password":$('#login-password').val()
        }),
    }).done(function(){
        document.location.reload(true);
    })
    .fail(function() {
        alert("authentication fail")
    });
    $('button.close').click();
}

function register(){
    console.log('registering');
    var request = $.ajax({
        url: "/apis/register",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "username":$('#register-username').val(),
            "password":$('#register-password').val(),
            "first_name":$('#first_name').val(),
            "last_name":$('#last_name').val(),
            "email":$('#register-email').val(),
        }),
        async: false,
        success : function(text)
        {
            if($('.writer-checkbox').prop( "checked")){
                var request_writer = $.ajax({
                    url: "/apis/writer_registration_list",
                    method: "POST",
                    contentType: "application/json",
                    dataType: "json",
                    data: JSON.stringify({
                        "description":$('#writer-text').val(),
                    }),
                })
            }
        }
    }).done(function(){
        location.href = "/"
    })
    .fail(function() {
        alert("unable to register")
    });
    $('button.close').click();
}

function edit_profile(user_id){
    if($('#register-password').val() != $('#confirm-password').val()){
        return alert('incorrect password');
    }
    var request = $.ajax({
        url: "/apis/edit_profile"+user_id,
        method: "PATCH",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "username":$('#account-username').val(),
            "password":$('#account-password').val(),
            "first_name":$('#first_name').val(),
            "last_name":$('#last_name').val(),
            "email":$('#setting-email').val(),

        }),
    }).done(function(){
        alert("success");
    })
    .fail(function() {
        alert("fail")
    });
}

function logout(){
    console.log('logging out');
    console.log('')
    var request = $.ajax({
        url: "/apis/logout",
        method: "GET",

    }).done(function(){
        location.href = "/"
    })
    .fail(function() {
        alert("authentication fail")
    });
    $('button.close').click();
}