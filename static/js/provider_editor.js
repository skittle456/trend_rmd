// var file;

// // Add events
// $('input[type=file]').on('change', prepareUpload);

// // Grab the files and set them to our variable
// function prepareUpload(event)
// {
//   file = event.target.files;
// }

function edit_provider_profile(provider_id){
    var request = $.ajax({
        url: "/apis/upload/image",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "file":file,
            "provider_id":provider_id,
        }),
    }).done(function(){
        alert("success");
    })
    .fail(function() {
        alert("fail")
    });
    // var request = $.ajax({
    //     url: "/apis/edit_provider_profile",
    //     method: "PATCH",
    //     contentType: "application/json",
    //     dataType: "json",
    //     data: JSON.stringify({
    //         "provider_name":$('input#provider_name.form-control').val(),
    //         "favicon_url":$('input#img-url.form-control').val()
    //     }),
    // }).done(function(){
    //     alert("success");
    // })
    // .fail(function() {
    //     alert("fail")
    // });
}