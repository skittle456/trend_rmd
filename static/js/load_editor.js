var quill = new Quill('#editor-container', {
    modules: {
        toolbar: [
        ['bold', 'italic'],
        ['link', 'blockquote', 'code-block', 'image', 'video'],
        [{ list: 'ordered' }, { list: 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'direction': 'rtl' }],                         // text direction

        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
      
        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'align': [] }],
      
        ['clean']        
        ]
    },
    placeholder: 'Write something...',
    theme: 'snow'
    });

function submitContent(){
    var request = $.ajax({
        url: "/apis/post",
        method: "PATCH",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "blog_content":content,
        }).done(function(){
            location.href = "/";
        })
        .fail(function() {
            alert('fail');
        })
    })
}

$(document).ready(function(){
    quill.root.innerHTML = content;
})

