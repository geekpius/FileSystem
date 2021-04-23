
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
                    swal('Success','Resend successful', 'success');
                }else{
                    if(resp.message.user){
                        swal('User', `${resp.message.user}`, 'warning');
                    }else if(resp.message.file){
                        swal('File', `${resp.message.file}`, 'warning');
                    }else{
                        swal('Error', `${resp.message}`, 'warning');
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
