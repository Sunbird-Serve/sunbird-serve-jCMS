$(document).ready(function() {
    //Board-wise Data Retrieval
    $(document).on('change','#boardFilterDropdownAdmin',function() {
        // $("#loader").removeClass("d-none");
        var boardId = $(this).val();
        var url = "/all_course/";
        var data ={boardId:boardId};
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });


    //Subject-wise Data Retrieval
    $(document).on('change','#subjectFilterDropdownAdmin',function() {
        // $("#loader").removeClass("d-none");
        var subjectId = $(this).val();
        var url = "/all_course/";
        var data ={subjectId:subjectId,boardId:selected_board};
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });

    //Search Courses
    $(document).on('click','#searchData', function(){
        var searchInput = $("#filterDataAdmin").val();
        var data ={searchInput:searchInput};
        var url = "/all_course/";
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    })



    $('#openModalBtn').on('click', function () {
        $('#modalTitle').html('Bulk Upload Course');
        $('#downloadTemplate').val('course');
        $('#fileUpload').val('course')
        $('#myModal').modal('show');
    });
    $('#closeModal').on('click', function () {
        $('#myModal').modal('hide');
    });

    $("#checkAll").click(function () {
        $(document).find('.singleCheckBox').not(this).prop('checked', this.checked);
    });

    $("#toggleCard").click(function() {
        var cardBody = $('#myCardBody');
        if (cardBody.css("display") === "none" || cardBody.css("display") === "none") {
            cardBody.css("display", "block");
        } else {
            cardBody.css("display", "none");
        }
    });

    $("#deleteAll").click(function(){
        $this = $(this);
        var numberIdsArray = [];
        $.each($("input[class='singleCheckBox']:checked"), function(){            
            numberIdsArray.push($(this).val());
        });

        if(numberIdsArray.length < 1){
            Swal.fire(
            'Required',
            'You must select one !!!',
            'warning'
            )
            return false;
        }
        data = {'delete':'course','numberIdsArray' : numberIdsArray};

        if (confirm("Are you sure, do you want to Detete?")) {
            // Get the CSRF token
            var csrftoken = $("[name=csrfmiddlewaretoken]").val();
            $.ajax({
                method: 'POST',
                url: "/deleteBulkData/",
                data:data,

                headers: { "X-CSRFToken": csrftoken }, // Include the CSRF token
                success: function(response) {
                    if (response == 'success') {
                        Swal.fire(
                            'Success',
                            'Course deleted successfully!',
                            'success',
                        )
                        // window.location.reload();
                    }setTimeout(() => {
                        window.location.reload();
                     }, 1000);
                }
            })
        }
    })


});
