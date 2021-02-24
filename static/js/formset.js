$(function(){
  $(document).on("click", ".btn-add", function(e){
    e.preventDefault();

    let form_name = $(this).data("form");
    let id_total_forms = "#id_"+form_name+"-TOTAL_FORMS";
    let form_idx = $(id_total_forms).val();
    let form = $("#"+form_name+"_form_set").append($("#"+form_name+"_empty_form").html().replace(/__prefix__/g, form_idx));
    console.log(form)
    $(id_total_forms).val(parseInt(form_idx) + 1);
    date();
  });

  $(document).on("click", ".btn-remove", function(e){
    e.preventDefault()
    let form_name = $(this).data("form");
    let id_total_forms = "#id_"+form_name+"-TOTAL_FORMS";
    let form_idx = $(id_total_forms).val();
    $(id_total_forms).val(parseInt(form_idx) - 1);
    
    row = $(this).closest(".row-remove")
    $(row).remove()
    let forms = $(".formset")
    
    // change id and name attributes after row deletion
    for (let i = 0; i < forms.length; i ++){
      console.log(i)
      let regex = new RegExp('('+form_name+'-\\d+)');
      let replacement = form_name + '-' + i;
      console.log(i)
      $(forms[i]).find(':input').each(function(pos, input){

        if (input.id) input.id = input.id.replace(regex, replacement)
        if (input.name) input.name = input.name.replace(regex, replacement)
      });
    }
  });
})