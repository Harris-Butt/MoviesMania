$(document).ready(function(){
    $('#load_more_movies').on('submit',function(){
        console.log( $(this))
        var form_ = $(this),
            url = form_.attr('action'),
            type = form_.attr('method')
            console.log(url)
            console.log(type)
        $.ajaxSetup({
            headers: { "X-CSRFToken": '{{csrf_token}}' }
            });
        $.ajax({
            type:type,
            url:url,
            success: function (data) {

             var parser = new DOMParser();
             data = parser.parseFromString(data,'text/html')
             console.log(data.body.innerHTML );
             $(".thumbnails").append(data.body.innerHTML);

            }
        })
        return false;

    });


});

