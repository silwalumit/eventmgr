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
                        window.location = "/"
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
                $("#form-modal-body").html(data);
                $("#modal-form").modal("show");
                ajaxFormSubmit("#form-modal-body form", "#modal-form")
            },
        });
    });
});