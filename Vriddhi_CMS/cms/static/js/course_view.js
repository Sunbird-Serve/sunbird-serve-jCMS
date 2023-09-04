
//Board-wise Data Retrieval
    $(document).ready(function() {
        $('#filterDropdown').change(function() {
            $("#loader").show();
            var boardId = $(this).val();
            var data ={boardId:boardId};
            $.get("/get_filtered_courses/",data,function(response,status){
                $("#courseContainer").html(response);

                var courses = response;
                $("#courseContainer").empty(); // Clear previous content

                for (var i = 0; i < courses.length; i++) {
                    var course = courses[i];
                    var courseCard = `
                        <div class="col-md-4 mb-4">
                            <div class="course-card course_details">
                                <input type="hidden" class="course_id" value="${course.id}">
                                <h5 class="course-title">${course.board}</h5>
                                <p class="course-detail"><strong>Subject:</strong> ${course.subject}</p>
                                <p class="course-detail"><strong>Grade:</strong> ${course.grade}</p>
                            </div>
                        </div>`;
                    $("#courseContainer").append(courseCard);
                }
                $("#loader").hide();
            })
        });


        //Content Details
        $(document).ready(function() {
            $(document).on('click', '.course_details', function() {
                var courseID = $(this).find('.course_id').val();
                window.location.href = '/home/view_content/?courseID=' + courseID;
            });
        });

        //Search Courses
        $(document).on('click','#searchData', function(){
            $("#loader").show();
            var searchInput = $("#filterData").val();
            var data ={searchInput:searchInput};
            $.get("/search_courses/", data, function(response,status){
                var courses = response;
                $("#courseContainer").empty(); // Clear previous content

                for (var i = 0; i < courses.length; i++) {
                    var course = courses[i];
                    var courseCard = `
                        <div class="col-md-4 mb-4">
                            <div class="course-card course_details">
                                <input type="hidden" class="course_id" value="${course.id}">
                                <h5 class="course-title">${course.board}</h5>
                                <p class="course-detail"><strong>Subject:</strong> ${course.subject}</p>
                                <p class="course-detail"><strong>Grade:</strong> ${course.grade}</p>
                            </div>
                        </div>`;
                    $("#courseContainer").append(courseCard);
                }
                $("#loader").hide();
            })
        })
    });
