(function($) {
    $(document).ready(function() {
        // Reference to the dropdowns
        var boardDropdown = $("#id_board"); 
        var courseDropdown = $("#id_course"); 
        var topicDropdown = $("#id_topic"); 

        courseDropdown.attr("disabled", "disabled");
        topicDropdown.attr("disabled", "disabled");

        boardDropdown.change(function() {

            var selectedBoardId = $(this).val();
            if (selectedBoardId) {
                courseDropdown.removeAttr("disabled");

                $.ajax({
                    url: "/get_courses/",  // URL to fetch courses
                    data: { board_id: selectedBoardId },
                    dataType: 'json',  // Specify the data type explicitly
                    success: function(data) {
                        // Clear and populate course dropdown
                        courseDropdown.empty();
                        courseDropdown.append($("<option></option>").attr("value", "").text("Select Course"));

                        $.each(data, function(index, course) {
                            dorpdownValue = course.board+'-'+course.name+'-'+course.grade;
                            courseDropdown.append($("<option></option>").attr("value", course.id).text(dorpdownValue));
                        });
                    },
                });
                
            } 
        });

        courseDropdown.change(function() {

            var selectedCourseId = $(this).val();
            if (selectedCourseId) {
                topicDropdown.removeAttr("disabled");

                $.ajax({
                    url: "/get_topics/",  // URL to fetch courses
                    data: { course_id: selectedCourseId },
                    dataType: 'json',  // Specify the data type explicitly
                    success: function(data) {
                        // Clear and populate course dropdown
                        topicDropdown.empty();
                        topicDropdown.append($("<option></option>").attr("value", "").text("Select Topic"));
                        $.each(data, function(index, topic) {
                            topicDropdown.append($("<option></option>").attr("value", topic.id).text(topic.name));
                        });
                    },
                });
                
            } 
        });


    });
})(django.jQuery);
