
 function processRequest() {
    console.log('request');
    $.ajax({
        url: window.location.href,
        type: "GET",
        success: function(resp, textStatus, jqXHR){
            if(jqXHR.status == 200){
                $(".onlineOffline").addClass('bg-success');
                $(".onlineOffline").text('Online');
            }else{
                $(".onlineOffline").removeClass('bg-success');
                $(".onlineOffline").text('Offline');
            }
        },
        error: function(resp){
            console.log('something wrong with request')
            $(".onlineOffline").removeClass('bg-success');
            $(".onlineOffline").text('Offline');
        }
    });
}

function getNotificationCount(){
    $.ajax({
       url: $('.notificationCount').data('url'),
       type: "GET",
       success: function(resp){
           if(resp.message ==='success'){
            $(".notificationCount").text(resp.notification_count);
           }else{
                $(".notificationCount").text('');
           }
       },
       error: function(resp){
           console.log('something wrong with request')
       }
   });
 }
 

function getNotification(){
   $.ajax({
      url: $('.notifications').data('url'),
      type: "GET",
      success: function(resp){
          $(".notifications").html(resp);
      },
      error: function(resp){
          console.log('something wrong with request')
      }
  });
}

function getMessages(){
    console.log('message');
   $.ajax({
      url: '',
      type: "GET",
      success: function(resp){
          $(".selector").html(resp);
      },
      error: function(resp){
          console.log('something wrong with request')
      }
  });
}

getNotificationCount();
getNotification();

setInterval(function(){
    getNotificationCount();
    getNotification();
    getMessages();
    processRequest();
}, 10000);