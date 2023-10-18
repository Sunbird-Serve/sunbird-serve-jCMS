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


    $('#openModalBtn').on('click', function () {
        $('#modalTitle').html('Bulk Upload Topic');
        $('#downloadTemplate').val('topic');
        $('#fileUpload').val('topic')
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
        data = {'delete':'topic','numberIdsArray' : numberIdsArray};

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
                            'Topic deleted successfully!',
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
