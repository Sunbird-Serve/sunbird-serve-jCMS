var player = videojs('my_video_player');
    var $x = $('#menu div').click(function() {
        $x.removeClass('selected');
        $(this).addClass('selected');
    })
    

    $('document').ready(function() {

        let video_id = document.getElementById('video1')
        if (video_id) {
            $('#no_video').hide()
            $('#my_video_player').show()
            video_id.click();
        } else {
            $('#no_video').show()
            $('#my_video_player').hide()
            //playVideo('https://youtu.be/4Y1aGTZGpCA', 'youtube', 'Introduction to eVidyaloka', 'eVidyaloka is a platform for students to learn and interact with the world of education.', 1);
        }
        $('#doubts_tab').click()
    });


    function playVideo(videoSource, type, title, description, id) {
        document.getElementById('current_video_title').innerHTML = title
        document.getElementById('current_video_description').innerHTML = description
        player.src({
            src: videoSource,
            //type: 'video/' + type
        });

        player.currentTime(50)
        player.muted(false);
        player.play();

        player.on('play', (event) => {
            update_video_playback(id, player.currentTime());
        });

        player.on('pause', (event) => {
            update_video_playback(id, player.currentTime());
        });

        $(".showVideo").css("background-image", 'url(' + thumbnailUrl + ')');

    }

    /*make_videos_table()
    function make_videos_table() {
        player.autoplay('muted');
        var title = '{{title}}';
    
        for (let index = 0; index < videos_data.length; index++) {
            const video = videos_data[index];
            let thumbnailUrl = '/static/img/video_placeholder.png'
            let type = "'mp4'"
            let duration = parseInt(video['duration'])
            if (duration) {
                duration = new Date(duration * 1000).toISOString().substr(11, 8)
            }

            if (video['contentHost'] == 'youtube') {
                type = "'youtube'"
            }

            let url = "'" + video["url"] + "'"
            let title = "'" + (video["title"]).replace("'", "") + "'"
            let description = "'" + (video["description"]).replace("'", "") + "'"
            let id = "'" + video["id"] + "'"
            //$('#flm_play_list').append('<div class="m-4 py-2 border-b hover:bg-gray-200 hover:text-green-500">\
            //                        <div class=" w-full flex">\
            //                            <div id="video' + index + '" onclick="playVideo(' + url + ', ' + type + ', ' + title + ', ' + description + ', ' + id + ')" class="cursor-pointer h-32 md:h-48 w-72 md:w-1/2 bg-contain md:bg-cover bg-center bg-no-repeat flex items-end justify-end" style="background-image: url(' + thumbnailUrl + ')" title="' + video['title'] + '"><p class="p-2 bg-blue-400 rounded-full text-base text-gray-800">' + duration + '</p></div>\
            //                            <div class="w-3/4 md:w-1/2 p-4 flex flex-col justify-between leading-normal">\
            //                                <div class="h-4">\
            //                                    <div class="font-bold text-xl md:text-3xl">' + video['title'] + '</div>\
            //                                </div>\
            //                                <div class="font-bold text-base md:text-xl">'+video['author']+'</div>\
            //                            </div>\
            //                        </div>\
            //                    </div>');
        }
    }
    


    function make_worksheet_table() {
       $('#content_wraper').show()
       $('#doubts_wraper').hide()
       player.pause();
       $("#content_details div").remove();
       if (worksheets_data.length > 0) {
       console.log("make_worksheet_table ",worksheets_data)
           for (let index = 0; index < worksheets_data.length; index++) {
               const worksheet = worksheets_data[index];
               let url = "'" + worksheet['url'] + "'"
               let id = "'" + worksheet['id'] + "'"

               $('#content_details').append('<div class="grid grid-flow-row grid-cols-2 md:grid-cols-6 gap-4 md:gap-16 items-center justify-center md:mx-48"><div class="h-96 w-64 md:w-72 flex flex-row border-2 border-gray-400 hover:border-blue-400  shadow-2xl bg-gradient-to-t from-gray-100 to-blue-200 rounded-l-lg rounded-r-3xl transform hover:z-50 hover:rotate-6 cursor-pointer" onclick="opendoc(' + url + ', ' + id + ')" style="background-image: url()" > \
                           <div class="h-full w-4 border-r-4 border-gray-500 border-dotted"></div>\
                           <div class="h-full mx-2 flex items-stretch justify-center">\
                               <p class="font-bold text-3xl self-start text-center py-20">' + worksheet['title'] + '</p>\
                           </div></div></div>')
           }
       } else {
           $('#content_details').append('<div class="text-center text-bold text-3xl"> No Content Available </div>')
       }
    }

    function make_textbook_table() {
       $('#content_wraper').show()
       $('#doubts_wraper').hide()
       player.pause();
       $("#content_details div").remove();
       if (textbooks_data.length > 0) {
           for (let index = 0; index < textbooks_data.length; index++) {
               const textbook = textbooks_data[index];
               let url = "'" + textbook['url'] + "'"

               $('#content_details').append('<div class="grid grid-flow-row grid-cols-2 md:grid-cols-6 gap-4 md:gap-16 items-center justify-center md:mx-48"><div class="h-96 w-64 md:w-72 flex flex-row border-2 border-gray-400  shadow-2xl bg-contain bg-center bg-no-repeat rounded-l-lg rounded-r-3xl transform hover:z-50 hover:rotate-6 cursor-pointer" onclick="window.open(' + url + ')" style="background-image: url()" > \
                           <div class="h-full w-4 border-r-4 border-gray-500 border-dotted"></div>\
                           <div class="h-full mx-2 flex items-stretch justify-center">\
                               <p class="font-bold text-3xl self-start text-center py-20">' + textbook['title'] + '</p>\
                           </div></div></div>')
           }
       } else {
           $('#content_details').append('<div class="text-center text-bold text-3xl py-42"> No Content Available </div>')
       }
    }


    function make_thirdparty_content_table() {
       $('#content_wraper').show()
       $('#doubts_wraper').hide()
       player.pause();
       $("#content_details div").remove();
       if (tpContentList.length > 0) {
       console.log("tpContentList ",tpContentList)
           for (let index = 0; index < tpContentList.length; index++) {
               const worksheet = tpContentList[index];
               let url = "'" + worksheet['url'] + "'"
               let id = "'" + worksheet['id'] + "'"

               $('#content_details').append('<div class="grid grid-flow-row grid-cols-2 md:grid-cols-6 gap-4 md:gap-16 items-center justify-center md:mx-48"><div class="h-96 w-64 md:w-72 flex flex-row border-2 border-gray-400 hover:border-blue-400  shadow-2xl bg-gradient-to-t from-gray-100 to-blue-200 rounded-l-lg rounded-r-3xl transform hover:z-50 hover:rotate-6 cursor-pointer" onclick="opendoc(' + url + ', ' + id + ')" style="background-image: url()" > \
                           <div class="h-full w-4 border-r-4 border-gray-500 border-dotted"></div>\
                           <div class="h-full mx-2 flex items-stretch justify-center">\
                               <p class="font-bold text-3xl self-start text-center py-20">' + worksheet['title'] + '</p>\
                           </div></div></div>')
           }
       } else {
           $('#content_details').append('<div class="text-center text-bold text-3xl"> No Content Available </div>')
       }
    }

    function update_video_playback(id, time) {
        if (time > 0) {
            let data = {
                "contentDetailsId": id,
                "offeringId": '{{offeringId}}',
                "topicId": '{{topicId}}',
                "subtopicId": subtopic_id,
                "progress": time
            }

            console.log('update_video_playback', data);
            $.ajax({
                type: "POST",
                url: "/v2/flm-content-view-status/",
                data: JSON.stringify(data),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(response) {
                    console.log(response)
                    if (response['status'] == 'success') {
                        // alert(response['data']['message'])
                        console.log('success')
                    } else if (response['status'] == 'error') {
                        alert(response['error']['message'])
                            // modalHandler()
                    }
                },
                failure: function(response) {
                    console.log(response)
                }
            });
        }

    };


    function opendoc(url, id) {
        window.open(url, '_blank');
        update_video_playback(id, 100);

    }*/


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }




    var video_rating = 0;
    var worksheet_rating = 0;
    $('.video__rating__star').click(function() {
        $('.video__rating__star').children().removeClass('text-orange-500');
        for (let index = 0; index < $(this).parent().children().length; index++) {
            if (index <= $(this).index()) {
                $(this).parent().children().eq(index).children().addClass('text-orange-500');
            }
        }
        video_rating = $(this).index() + 1;

    });
    $('.workbook__rating__star').click(function() {
        $('.workbook__rating__star').children().removeClass('text-orange-500');
        for (let index = 0; index < $(this).parent().children().length; index++) {
            if (index <= $(this).index()) {
                $(this).parent().children().eq(index).children().addClass('text-orange-500');
            }
        }
        worksheet_rating = $(this).index() + 1;
    });

    function submit_rating() {
        let data = {
            "topicId": topicId,
            "subtopicId": subtopic_id,
            "videoRating": video_rating,
            "worksheetRating": worksheet_rating,
            "comment": $('#comment').val()
        }

        if (data['videoRating'] == 0 || data['worksheetRating'] == 0) {
            alert('Please rate the video and worksheet')
        } else {
            
            $.ajax({
                type: "POST",
                url: "/subtopic/content_rating/",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                data: data,
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(response) {
                    if (response['status'] == 'success') {
                        alert(response['message'])
                        $('#rating_pop').hide()
                    } else if (response['status'] == 'error') {
                        alert(response['error']['message'])
                            // modalHandler()
                    }
                },

            });
        }

    }