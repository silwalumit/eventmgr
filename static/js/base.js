$(function(){
  toast();
  time();
  date();

});

var toast = ()=> $(".toast").toast('show');
var time = ()=>$('.timepicker').datetimepicker({
    datepicker: false,
    format: 'H:m'  
  });

// datepicker
var date = () => $(".datepicker").datetimepicker({
  timepicker: false,
  format:'Y-m-d'
});