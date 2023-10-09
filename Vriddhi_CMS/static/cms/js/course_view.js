$(document).ready(function() {
    //Board-wise Data Retrieval
    $(document).on('change','#boardFilterDropdown',function() {
        // $("#loader").removeClass("d-none");
        var boardId = $(this).val();
        var url = "/home/view_course/";
        var data ={boardId:boardId};
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });


    //Subject-wise Data Retrieval
    $(document).on('change','#subjectFilterDropdown',function() {
        // $("#loader").removeClass("d-none");
        var subjectId = $(this).val();
        var url = "/home/view_course/";
        var data ={subjectId:subjectId,boardId:selected_board};
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });

    //Search Courses
    $(document).on('click','#searchData', function(){
        // $("#loader").removeClass("d-none");
        if($("#filterData").val() != undefined){
            var searchInput = $("#filterData").val();
            var data ={searchInput:searchInput};
            var url = "/home/view_course/";
            var queryString = $.param(data);
            window.location.href = url + '?' + queryString;
        }else{
            var searchInput = $("#filterDataAdmin").val();
            var data ={searchInput:searchInput};
            var url = "/all_course/";
            var queryString = $.param(data);
            window.location.href = url + '?' + queryString;
        }
    })



    //Content Details
    $(document).ready(function() {
        $(document).on('click', '.course_details', function() {
            var courseID = $(this).find('.course_id').val();
            window.location.href = '/home/view_content/?courseID=' + courseID;
        });
    });


});
