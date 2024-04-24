$(document).ready(function() {
    console.log("JS File Loaded");
    // Board-wise Data Retrieval
    $('#boardFilterDropdown').on('change', function() {
        var boardName = $(this).val(); 
        console.log('Board Name:', boardName); 
        var url = "/home/view_course/";
        var data = {boardId: boardName}; // Use boardName directly
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });

    // Subject-wise Data Retrieval
    $('#subjectFilterDropdown').on('change', function() {
        var subjectName = $(this).val(); // Correct variable name
        var boardName = $('#boardFilterDropdown').val(); // Get the current value of the board filter
        console.log('Subject Name:', subjectName, 'Board Name:', boardName);
        var url = "/home/view_course/";
        var data = {subjectId: subjectName, boardId: boardName}; // Use subjectName and boardName directly
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });

    // Search Courses
    $('#searchData').on('click', function() {
        var searchInput = $("#filterData").val();
        console.log('Search Input:', searchInput);
        var url = "/home/view_course/";
        var data = {searchInput: searchInput}; // Correct variable names
        var queryString = $.param(data);
        window.location.href = url + '?' + queryString;
    });

    // Content Details
    $('.course_details').on('click', function() {
        var courseID = $(this).find('.course_id').val();
        console.log('Course ID:', courseID);
        window.location.href = '/home/view_content/?courseID=' + courseID;
    });
});
