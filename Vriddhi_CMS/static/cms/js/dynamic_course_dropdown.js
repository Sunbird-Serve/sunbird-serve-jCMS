(function($) {
    $(document).ready(function() {
        // Reference to the dropdowns
        var currentURL = window.location.href;

        var boardDropdown = $("#id_board"); 
        var courseDropdown = $("#id_course");
        var topicDropdown = $("#id_topic"); 
        var subTopicDropdown = $("#id_subtopic")

        courseDropdown.attr("disabled", "disabled");
        topicDropdown.attr("disabled", "disabled");
        subTopicDropdown.attr("disabled", "disabled");

        if (currentURL.indexOf("/admin/cms/contentdetail/add/") !== -1) {
            topicDropdown.attr("disabled", false);
        }else{
            topicDropdown.attr("disabled", true);
        }

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

        topicDropdown.change(function() {

            var selectedTopicId = $(this).val();
            if (selectedTopicId) {
                subTopicDropdown.removeAttr("disabled");

                $.ajax({
                    url: "/get_subTopics/",  // URL to fetch courses
                    data: { topic_id: selectedTopicId },
                    dataType: 'json',  // Specify the data type explicitly
                    success: function(data) {
                        // Clear and populate course dropdown
                        subTopicDropdown.empty();
                        subTopicDropdown.append($("<option></option>").attr("value", "").text("Select Topic"));
                        $.each(data, function(index, subTopic) {
                            subTopicDropdown.append($("<option></option>").attr("value", subTopic.id).text(subTopic.name));
                        });
                    },
                });
                
            } 
        });


    });
})(django.jQuery);
