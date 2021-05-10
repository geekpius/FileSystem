
$(".datatable-basic tbody tr").on('click', '.resend', function(e){
    e.preventDefault();
    e.stopPropagation();
    var $this = $(this);
    swal({
        title: "Sure to resend?",
        text: `You are about resend to ${$this.parents('.record').find('td').eq(1).text()}`,
        type: "warning",
        showCancelButton: true,
        confirmButtonClass: "btn-sm text-success",
        cancelButtonClass: "btn-sm",
        confirmButtonText: "Yes, resend",
        closeOnConfirm: true
        },
    function(){
        let data = {
            csrfmiddlewaretoken: $this.data('token'),
            file: $this.data('id'),
            user: $this.data('user'),
            status: $this.data('status'),
        }
        $.ajax({
            url: $this.attr('href'),
            type: "POST",
            data: data,
            dataType: "json",
            success: function(resp){
                if(resp.message==='success'){
                    let inter = setInterval(function(){
                        alert('Resend successful');
                        clearInterval(inter);
                    },100);
                }else{
                    if(resp.message.user){
                        let inter = setInterval(function(){
                            alert(resp.message.user);
                            clearInterval(inter);
                        },100);
                    }else if(resp.message.file){
                        let inter = setInterval(function(){
                            alert(resp.message.file);
                            clearInterval(inter);
                        },100);
                    }else{
                        let inter = setInterval(function(){
                            alert(resp.message);
                            clearInterval(inter);
                        },100);
                    }
                }
            },
            error: function(resp){
                console.log('something wrong with request')
            }
        });
    });
  return false;
});
