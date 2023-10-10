$(document).ready(function() {
    //Board-wise Data Retrieval
    $(document).on('change','#boardFilterDropdownAdmin',function() {
        // $("#loader").removeClass("d-none");
        var boardId = $(this).val();
        var url = "/all_topic/";
        var data ={boardId:boardId};
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });


    //Subject-wise Data Retrieval
    $(document).on('change','#subjectFilterDropdownAdmin',function() {
        // $("#loader").removeClass("d-none");
        var subjectId = $(this).val();
        var url = "/all_topic/";
        var data ={subjectId:subjectId,boardId:selected_board};
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });

    //Topic-wise Data Retrieval
    $(document).on('change','#topicFilterDropdownAdmin',function() {
        // $("#loader").removeClass("d-none");
        var topicId = $(this).val();
        var url = "/all_topic/";
        var data ={topicId:topicId,boardId:selected_board, subjectId:selected_subjectId};
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });

    //Search Courses
    $(document).on('click','#searchData', function(){
        var searchInput = $("#filterDataAdmin").val();
        var data ={searchInput:searchInput};
        var url = "/all_topic/";
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    })

    //Search Courses
    $(document).on('click','#', function(){
        var searchInput = $("#filterDataAdmin").val();
        var data ={searchInput:searchInput};
        var url = "/all_topic/";
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    })
    



    // //Content Details
    // $(document).ready(function() {
    //     $(document).on('click', '.course_details', function() {
    //         var courseID = $(this).find('.course_id').val();
    //         window.location.href = '/home/view_content/?courseID=' + courseID;
    //     });
    // });


});
