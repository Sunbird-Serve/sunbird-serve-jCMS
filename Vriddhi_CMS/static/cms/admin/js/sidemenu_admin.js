$(document).ready(function() {
    $(document).on('click','#course_menu', function(){
        var url = "/all_course/";
        window.location.href = url ;
    })
    $(document).on('click','#topic_menu', function(){
        var url = "/all_topic/";
        window.location.href = url ;
    })
    $(document).on('click','#subtopic_menu', function(){
        var url = "/all_subtopic/";
        window.location.href = url ;
    })
    $(document).on('click','#content_menu', function(){
        var url = "/all_content/";
        window.location.href = url ;
    })
});