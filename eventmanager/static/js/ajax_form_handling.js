$(function () {
    let ajaxFormSubmit = function(form, modal) {
        $(form).submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                success: function (xhr, status, thrownError) {
                    if ( $(xhr).find('.invalid-feedback').length > 0 ) {
                        
                        $(modal).find('.modal-body').html(xhr);
                        
                        $('.invalid-feedback').css({
                            'display': 'block',
                            'font-weight':800
                        });
                        ajaxFormSubmit(form, modal);
                    } else {
                        $(modal).modal('toggle');
                    }
                },
            });
        });
    }

    $(document).on("click", ".show-form", function(event) {
        event.preventDefault();
        let title = $(this).attr("title")
        let cls = $(this).data("class")
        $.ajax({
            url: $(this).attr('href'),
            type: 'GET',
            dataType: 'html',
            beforeSend: function(){
                $(".modal-dialog").removeClass('modal-sm').addClass(cls);
                $(".modal-title").html(title)
            },
            success: function(data, status, jqXHR){  
                $("#modal-form").modal("show");
                $("#form-modal-body").html(data);

                ajaxFormSubmit("#form-modal-body form", "#modal-form")
            },

            error:function(data, status, jqXHR){
                console.log(data, status, jqXHR);
            },
        });
    });
});