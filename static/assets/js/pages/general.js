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