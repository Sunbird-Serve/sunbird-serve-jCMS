//Show topic details
function make_topics_table(topics,subtopics) {
    $("#topic_name").empty(); 
    $("#topic_name").append(`<b>${topic_name}</b>`);
    $("#topics div").remove();

    for (let index = 0; index < topics.length; index++) {
        const topic = topics[index];
        let id = 'topicdiv_' + topic["id"];
        let active = '';
        if (index == 0) {
            active = 'default_topic'
        }

        $("#topics").append('<div id="' + id + '" tabindex="' + (index + 1) + '" onclick="subtopic(' + topic["id"] + ')" class="' + active + ' flex w-full cursor-pointer border-b-2 border-l-0 hover:border-l-2 border-gray-400 hover:bg-purple-300 font-bold">\
                                <div class="w-1/5 text-center text-xl p-4">' + (index + 1) + '</div>\
                                <div class="w-4/5 text-left text-cneter p-2">\
                                <p id="topic_' + topic["id"] + '">' + topic["name"] + '</p>\
                                </div></div>')

    }


    $("#subtopicsDetails").empty(); 

    for(let index = 0; index < subtopics.length; index++){
        const subtopic = subtopics[index];

        let click = "location.href='/subtopic/content-details/?subtopic_id=" + subtopic["subtopic_ids"] + "&topic_id=" + subtopic["topic_id"] + "'"
        let onclick = 'onclick="popup(' + subtopic["subtopic_ids"] + ')"'
        
        let button = `<button class="bg-purple-500 text-white active:bg-purple-600 font-bold uppercase text-xs px-4 md:px-4 py-2 rounded shadow focus:outline-none mr-1 mb-2 mt-2 ease-linear transition-all duration-150 content-view-button" type="button" onclick="${click}" >view content</button>`

        var subTopicTableData = '<tr class="border-b-2 subtopic hover:bg-gray-100">\
            <td class="text-center text-xl p-2 mobile_hide">1</td>\
            <td class="p-2 text-left subtopic-cell" rowspan="1">'+subtopic["subtopic_names"]+'</td>\
            <td class="">'+`${button}`+'</td>\
            <td class="p-2 text-left subtopic-cell" rowspan="1">'+subtopic["subtopic_statuses"]+'</td>';
        
        subTopicTableData += `</tr>`;
        $("#subtopicsDetails").append(subTopicTableData);

        $("#topic_name").empty(); 
        $("#topic_name").append(`<b>${subtopic.topic_names}</b>`);
    }
    $('#subtopics_length').empty();
    $('#subtopics_length').append("(" + subtopics.length + ")")


}

//Get subtopic details
function subtopic(topicId) {
    make_subtopics_table(topics, topicId)
}

function make_subtopics_table(topics, topicId) {

    $("#subtopicsDetails").empty();
    var data = {topicId: topicId}
    $.get('/home/getSubtopic/',data,function(response,status){
        var subtopics = response

        $('#subtopics_length').empty();
        $('#subtopics_length').append("(" + subtopics.length + ")");

        for (let index = 0; index < subtopics.length; index++) {
            var subtopic = subtopics[index];

            let click = "location.href='/subtopic/content-details/?subtopic_id=" + subtopic.id + "&topic_id=" + topicId + "'"
            let onclick = 'onclick="popup(' + subtopic["id"] + ')"'


            let button = `<button class="bg-purple-500 text-white active:bg-purple-600 font-bold uppercase text-xs px-4 md:px-4 py-2 rounded shadow focus:outline-none mr-1 mb-2 mt-2 ease-linear transition-all duration-150 content-view-button" type="button" onclick="${click}" >view content</button>`



            var subTopicTableData = `<tr id="" class="border-b-2 subtopic hover:bg-gray-100">
                <td class="text-center text-xl p-2 mobile_hide">${index + 1}</td>
                <td class="p-2 text-left subtopic-cell" rowspan="1">${subtopic.name}</td>
                <td class="">${button}</td>
                <td class="p-2 text-left subtopic-cell" rowspan="1">${subtopic.status}</td>`;
            
            subTopicTableData += `</tr>`;
            $("#subtopicsDetails").append(subTopicTableData);
            // $('#subtopics_length').append("(" + subtopic["subtopics"].length + ")")
            // document.getElementById('subtopics_length').innerHTML = "(" + subtopic["subtopics"].length + ")"

            $("#topic_name").empty(); 
            $("#topic_name").append(`<b>${subtopic.topic_name}</b>`);
        }
    })
}