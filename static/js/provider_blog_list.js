function getBlog(url,blog_id){
    console.log('getting blog');
    // var request = $.ajax({
    //     url: 'apis/add_view/'+blog_id,
    //     type: 'GET',
    // });
    if(url.search('/clog/'+blog_id) == 0){
        window.location.href = url;
    }
    else {
        window.open(url,'_blank');
    }
    return false;
}