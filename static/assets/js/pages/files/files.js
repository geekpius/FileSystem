
$("#formFile").on("submit", function(e){
    e.stopPropagation();
    e.preventDefault();
    var $this = $(this);
    var formData = new FormData(this);
    var valid = true;
    $('#formFile input, #formFile select').each(function() {
        let $this = $(this);
        
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('name').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if(valid){
        $("#formFile .btnSubmit").html('<i class="fa fa-spin fa-spinner"></i> Submitting...').attr('disabled',true);
        $.ajax({
            url: $("#formFile").attr("action"),
            type: "POST",
            dateType: "json",
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(resp){
                if(resp.message==='success'){
                    swal({
                        title: "Success",
                        text: `File is created successful`,
                        type: "success",
                        showCancelButton: false,
                        confirmButtonClass: "btn-sm text-primary",
                        confirmButtonText: "Okay",
                        },
                    function(){
                        $("#formFile")[0].reset();
                        $("#formFile input[name='name']").focus();
                    });
                }else{
                    if(resp.message.name){
                        swal('Name', `${resp.message.name}`, 'warning');
                    }else if(resp.message.file){
                        swal('File', `${resp.message.file}`, 'warning');
                    }else{
                        swal('Error', `${resp.message}`, 'warning');
                    }
                }
                $("#formFile .btnSubmit").html('Submit <i class="fa fa-dot-circle font-size-sm ml-2"></i>').attr('disabled',false);
            },
            error: function(resp){
                console.log('something wrong with request')
                $("#formFile .btnSubmit").html('Submit <i class="fa fa-dot-circle font-size-sm ml-2"></i>').attr('disabled',false);
            }
        });
    }
    return false;
});


$("#formFile select[name='zone']").on("change", function(e){
    e.stopPropagation();
    e.preventDefault();
    var $this = $(this);
    if($this.val() != ''){
        let data = {
            csrfmiddlewaretoken: $this.data('token'),
            zone: $this.val()
        }
        $.ajax({
        url: $this.data('url'),
        type: "POST",
        dateType: "json",
        data: data,
        success: function(resp){
            if(resp.message === 'success'){
                let options = '';
                resp.data.forEach(department => {
                    options+='<option value='+department.name+'>'+department.name +'</option>';
                });
                $("#formFile select[name='department']").find('.after').after(options);
            }
            else{
                $("#formFile select[name='department']").find('.after').nextAll().remove();
            }
        },
        error: function(resp){
            console.log('something wrong with request')
        }
    });
    }else{
        $("#formFile select[name='department']").find('.after').nextAll().remove();
    }
    return false;
});


$("#formFile select[name='department']").on("change", function(e){
    e.stopPropagation();
    e.preventDefault();
    var $this = $(this);
    if($("#formFile select[name='zone']").val() != '' && $this.val() != ''){
        let data = {
            csrfmiddlewaretoken: $this.data('token'),
            zone: $("#formFile select[name='zone']").val(),
            department: $this.val()
        }
        $.ajax({
        url: $this.data('url'),
        type: "POST",
        dateType: "json",
        data: data,
        success: function(resp){
            if(resp.message === 'success'){
                let options = '';
                resp.data.forEach(receiver => {
                    options+=`<option value="${receiver.id}">${receiver.name} (${receiver.account_type.toUpperCase()})</option>`;
                });
                $("#formFile select[name='receiver']").find('.after').after(options);
            }
            else{
                $("#formFile select[name='receiver']").find('.after').nextAll().remove();
            }
        },
        error: function(resp){
            console.log('something wrong with request')
        }
    });
    }else{
        $("#formFile select[name='receiver']").find('.after').nextAll().remove();
    }
    return false;
});


$(".datatable-basic tbody tr").on('click', '.btnChange', function(e){
    e.preventDefault();
    e.stopPropagation();
    var $this = $(this);
    $("#changeModal .modal-title").text(`Change ${$this.parents('.record').find('td').eq(2).text()} file`);
    $("#formChange input[name='file_id']").val($this.data('id'));
    $("#formChange select[name='status']").val($this.data('status'));
    $("#changeModal").modal('show');
    return false;
});


$("#formChange").on("submit", function(e){
    e.stopPropagation();
    e.preventDefault();
    var $this = $(this);
    var valid = true;
    $('#formChange select').each(function() {
        let $this = $(this);
        
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('name').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if(valid){
        $("#formChange .btnEdit").text('Saving Changes...').attr('disabled',true);
        let data = $this.serialize();
        $.ajax({
            url: $("#formChange").attr("action"),
            type: "POST",
            dateType: "json",
            data: data,
            success: function(resp){
                if(resp.message==='success'){
                    swal({
                        title: "Changed",
                        text: `Status changed successful`,
                        type: "success",
                        showCancelButton: false,
                        confirmButtonClass: "btn-sm text-primary",
                        confirmButtonText: "Okay",
                        },
                    function(){
                        $("#changeModal").modal('hide');
                        window.location.reload();
                    });

                }else{
                    swal('Error', `${resp.message}`, 'warning');
                }
                $("#formChange .btnEdit").text('Save changes').attr('disabled',false);
            },
            error: function(resp){
                console.log('something wrong with request')
                $("#formChange .btnEdit").text('Save changes').attr('disabled',false);
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
                // alert(resp.message)
                if(resp.message === 'success'){
                    alert('yes');
                }else{
                    alert('no');
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





$("#formFile input, #formChange input").on('input', function(){
    if($(this).val()!=''){
        $(this).parents('.validate').find('.mySpan').text('');
    }else{ $(this).parents('.validate').find('.mySpan').text('The '+$(this).attr('name').replace(/[\_]+/g, ' ')+' field is required'); }
});

$("#formFile select, #formChange select").on('change', function(){
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