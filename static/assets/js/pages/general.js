var xhr = new XMLHttpRequest();
 //index.php is in my web
 xhr.open('GET', 'https://www.google.com', true);
 xhr.send();

 xhr.addEventListener("readystatechange", processRequest, false);

 function processRequest(e) {
     if (xhr.readyState == 4) {
         if (xhr.status >= 200 && xhr.status < 304) {
            $(".onlineOffline").addClass('bg-success');
            $(".onlineOffline").text('Online');
         } else {
            $(".onlineOffline").removeClass('bg-success');
            $(".onlineOffline").text('Offline');
         }
     }
}

function getNotification(){
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

function getMessages(){
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

setTimeout(function () { getNotification(); getMessages(); }, 5000);