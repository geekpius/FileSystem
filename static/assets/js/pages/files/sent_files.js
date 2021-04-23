
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
        // $.ajax({
        //     url: $this.attr('href'),
        //     type: "GET",
        //     dataType: "json",
        //     success: function(resp){
        //         if(resp.message==='success'){
        //             $this.parents('.record').fadeOut('slow', function(){
        //                 $this.parents('.record').remove();
        //             });
        //         }else{
        //             console.log("something went wrong");
        //         }
        //     },
        //     error: function(resp){
        //         console.log('something wrong with request')
        //     }
        // });
    });
  return false;
});
