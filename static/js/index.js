// jQuery(function($) {
//     $("img.lazy").lazyload({
//     threshold: 50,
//     data_attribute: "orig"
// });
// $(window).trigger("scroll");
// });
var blogs = null;
$('div#demo').on('slide.bs.carousel', function (e) {
        var $e = $(e.relatedTarget);
        var idx = $e.index();
        var itemsPerSlide = 1;
        var totalItems = $('.carousel-item').length;
        
        if (idx >= totalItems-(itemsPerSlide-1)) {
            var it = itemsPerSlide - (totalItems - idx);
            for (var i=0; i<it; i++) {
                // append slides to end
                if (e.direction=="left") {
                    $('.carousel-item').eq(i).appendTo('.carousel-inner');
                }
                else {
                    $('.carousel-item').eq(0).appendTo('.carousel-inner');
                }
            }
        }
    });
function reload_elements(){
    pathName = window.location.pathname;
    var element_selected = $('.on-selected');
    element_selected.removeClass('on-selected');
    var element_tagged = $(".on-tagged");
    element_tagged.removeClass("on-tagged");
    var category_name  = $('.nav-category').val();
    if (location.pathname == "/") {
        //$('#feed').addClass('on-selected');
        $('#feed').addClass('on-tagged');
    }
    if (pathName.search("/category/"+category_name+"/tag/") != -1){
        let tagName = pathName.substring(pathName.lastIndexOf('/') + 1);
        $( "#"+category_name ).addClass( "on-selected" );
        $("#"+tagName).addClass( "on-tagged");
        $("#tag-"+tagName).prependTo(".tag-bar");
        $(".nav-tag").animate({ scrollLeft: 0 }, "slow");
        return false;
    }
    else if (pathName.search("/category/"+category_name) != -1){
      let categoryName = pathName.substring(pathName.lastIndexOf('/') + 1);
      $( "#"+categoryName ).addClass( "on-selected" );
    }
    else if (pathName.search("tag") != -1){
        let tagName = pathName.substring(pathName.lastIndexOf('/') + 1);
        //$('#feed').addClass('on-selected');
        $("#"+tagName).addClass( "on-tagged");
        //$("#tag-"+tagName).prependTo(".tag-bar");
        //$(".nav-tag").animate({ scrollLeft: 0 }, "slow");
        return false;
      }
    else if (pathName.search("provider") != -1){
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
function resetNav(){
    var nav = $('.mainbar');
    var nav_category = $('.nav-category');
    var nav_tag = $('.nav-tag');
    nav.fadeIn(1);
    nav_category.removeClass('fixed');
    nav_tag.removeClass('tag-fixed');
    nav_category.removeClass('nav-ontop-category');
    nav_tag.removeClass('nav-ontop-tag');
}