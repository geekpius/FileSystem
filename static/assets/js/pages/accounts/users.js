
// $('.datatable-basic').DataTable();

$(".btnAdd").on('click', function(){


});

$("#formUser").on("submit", function(e){
    e.stopPropagation();
    e.preventDefault();
    var $this = $(this);
    var valid = true;
    $('#formUser input, #formUser select').each(function() {
        let $this = $(this);
        
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('name').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if(valid){
        $("#formUser .btnSubmit").html('<i class="fa fa-spin fa-spinner"></i> Submitting...').attr('disabled',true);
        let data = $this.serialize();
        $.ajax({
            url: $("#formUser").attr("action"),
            type: "POST",
            dateType: "json",
            data: data,
            success: function(resp){
                if(resp.message==='success'){
                    swal({
                        title: "Success",
                        text: `User is created successful`,
                        type: "success",
                        showCancelButton: false,
                        confirmButtonClass: "btn-sm text-primary",
                        confirmButtonText: "Okay",
                        },
                    function(){
                        $("#formUser")[0].reset();
                        $("#formUser input[name='email']").focus();
                    });
                }else{
                    if(resp.message.email){
                        swal('Error', `${resp.message.email}`, 'warning');
                    }else if(resp.message.name){
                        swal('Error', `${resp.message.name}`, 'warning');
                    }else if(resp.message.phone){
                        swal('Error', `${resp.message.phone}`, 'warning');
                    }else if(resp.message.zone){
                        swal('Error', `${resp.message.zone}`, 'warning');
                    }
                }
                $("#formUser .btnSubmit").html('Submit <i class="fa fa-dot-circle font-size-sm ml-2"></i>').attr('disabled',false);
            },
            error: function(resp){
                console.log('something wrong with request')
                $("#formUser .btnSubmit").html('Submit <i class="fa fa-dot-circle font-size-sm ml-2"></i>').attr('disabled',false);
            }
        });
    }
    return false;
});


$(".datatable-basic tbody tr").on('click', '.btnDelete', function(e){
    e.preventDefault();
    e.stopPropagation();
    var $this = $(this);
    swal({
        title: "Sure to delete?",
        text: `You are about delete ${$this.parents('.record').find('td').eq(1).text()} account`,
        type: "warning",
        showCancelButton: true,
        confirmButtonClass: "btn-sm text-danger",
        cancelButtonClass: "btn-sm",
        confirmButtonText: "Yes, delete",
        closeOnConfirm: true
        },
    function(){
        $.ajax({
            url: $this.attr('href'),
            type: "GET",
            dataType: "json",
            success: function(resp){
                if(resp.message==='success'){
                    $this.parents('.record').fadeOut('slow', function(){
                        $this.parents('.record').remove();
                    });
                }else{
                    console.log("something went wrong");
                }
            },
            error: function(resp){
                console.log('something wrong with request')
            }
        });
    });
  return false;
});


$(".datatable-basic tbody tr").on('click', '.btnDeactivate', function(e){
    e.preventDefault();
    e.stopPropagation();
    var $this = $(this);
    let color = $this.data('status').toLowerCase() == 'activate'? 'text-success':'text-danger';
    swal({
        title: `Sure to ${$this.data('status').toLowerCase()}?`,
        text: `You are about deactivate ${$this.parents('.record').find('td').eq(1).text()} zone`,
        type: "warning",
        showCancelButton: true,
        confirmButtonClass: `btn-sm ${color}`,
        cancelButtonClass: "btn-sm",
        confirmButtonText: `Yes, ${$this.data('status').toLowerCase()}`,
        closeOnConfirm: true
        },
    function(){
        $.ajax({
            url: $this.attr('href'),
            type: "GET",
            dataType: "json",
            success: function(resp){
                if(resp.message === 'success'){
                    let inter = setInterval(function(){
                        alert(`${$this.parents('.record').find('td').eq(1).text()} account is ${$this.data('status').toLowerCase()}d successful`);
                        window.location.reload();
                        clearInterval(inter);
                    },100);
                }else{
                    console.log("something went wrong");
                }
                // if(resp.message === 'success'){
                //     swal({
                //         title: `${$this.data('status').toLowerCase()}d`,
                //         text: `${$this.parents('.record').find('td').eq(1).text()} zone is ${$this.data('status').toLowerCase()}d successful`,
                //         type: "success",
                //         showCancelButton: false,
                //         confirmButtonClass: `btn-sm text-primary`,
                //         confirmButtonText: `Okay`,
                //         closeOnConfirm: true
                //         },
                //     function(){
                //         window.location.reload();
                //     });
                // }else{
                //     console.log("something went wrong");
                // }
            },
            error: function(resp){
                console.log('something wrong with request')
            }
        });
    });
  return false;
});



$("#formProfile").on("submit", function(e){
    e.stopPropagation();
    e.preventDefault();
    var $this = $(this);
    var valid = true;
    $('#formProfile input, #formProfile select').each(function() {
        let $this = $(this);
        
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('name').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if(valid){
        $("#formProfile .btnSubmit").html('Saving Changes...').attr('disabled',true);
        let data = $this.serialize();
        $.ajax({
            url: $("#formProfile").attr("action"),
            type: "POST",
            dateType: "json",
            data: data,
            success: function(resp){
                if(resp.message==='success'){
                    swal('Updated', 'Profile updated successful', 'success');
                }else{
                    if(resp.message.email){
                        swal('Error', `${resp.message.email}`, 'warning');
                    }else if(resp.message.name){
                        swal('Error', `${resp.message.name}`, 'warning');
                    }else if(resp.message.phone){
                        swal('Error', `${resp.message.phone}`, 'warning');
                    }else if(resp.message.zone){
                        swal('Error', `${resp.message.zone}`, 'warning');
                    }else{
                        swal('Error', `${resp.message}`, 'warning');
                    }
                }
                $("#formProfile .btnSubmit").html('Save changes').attr('disabled',false);
            },
            error: function(resp){
                console.log('something wrong with request')
                $("#formProfile .btnSubmit").html('Save changes').attr('disabled',false);
            }
        });
    }
    return false;
});


$("#formChangePassword").on("submit", function(e){
    e.preventDefault();
    e.stopPropagation();
    var valid = true;
    var $this = $(this);
    $('#formChangePassword input:password').each(function() {
        let $this = $(this);
        if($this.attr('id')=='password'){
            if($this.val().length<6){
                valid = false;
                $this.parents('.validate').find('.mySpan').text('Password field must be more than 6 characters');
            }
        }
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('id').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if($("#password_confirmation").val()!=$("#password").val()){
        valid = false;
        $("#password_confirmation").parents('.validate').find('.mySpan').text('Password does not match');
    }

    if(valid) {
        $('.btnChangePassword').html('<i class="fa fa-spinner fa-spin"></i> CHANGING PASSWORD...').attr('disabled', true);
        let data = $this.serialize();
        $.ajax({
            url: $this.attr('action'),
            type: "POST",
            dataType: 'json',
            data: data,
            success: function(response){
                if(response.message=='success'){
                    swal({
                        title: "Changed",
                        text: "Your password is changed successful",
                        type: "success",
                        confirmButtonClass: "btn-success btn-sm",
                        cancelButtonClass: "btn-sm",
                        confirmButtonText: "Okay",
                        closeOnConfirm: true
                        },
                    function(){
                        $("#formChangePassword #current_password").val('');
                        $("#formChangePassword #password").val('');
                        $("#formChangePassword #password_confirmation").val('');
                    });
                }else{
                    let text = "";
                    $.map( response, function( val, i ) {
                        let old = (val.old_password==undefined)? '': val.old_password;
                        let newp = (val.new_password2==undefined)? '': val.new_password2;
                        text+=old+'\n'+newp;
                    });

                    $("#msgContainer").text(text);
                    $("#formChangePassword #current_password").val('').focus();
                    $("#formChangePassword #password").val('');
                    $("#formChangePassword #password_confirmation").val('');
                }
                $('.btnChangePassword').html('<i class="fa fa-refresh"></i> CHANGE PASSWORD').attr('disabled', false);
            },
            error: function(response){
                console.log('something wrong with request')
                $('.btnChangePassword').html('<i class="fa fa-refresh"></i> CHANGE PASSWORD').attr('disabled', false);
            }
        });
    }
    return false;
});


$("#formUser input, #formChangePassword input, #formProfile input").on('input', function(){
    if($(this).val()!=''){
        $(this).parents('.validate').find('.mySpan').text('');
    }else{ $(this).parents('.validate').find('.mySpan').text('The '+$(this).attr('name').replace(/[\_]+/g, ' ')+' field is required'); }
});

$("#formUser select, #formProfile select").on('change', function(){
    if($(this).val()!=''){
        $(this).parents('.validate').find('.mySpan').text('');
    }else{ $(this).parents('.validate').find('.mySpan').text('The '+$(this).attr('name').replace(/[\_]+/g, ' ')+' field is required'); }
});

function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}
  
$("#formProfile select[name='zone']").val($("#formProfile select[name='zone']").data('selected'));