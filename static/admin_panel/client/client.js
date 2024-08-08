 $('#filter').on('cancel.daterangepicker',function () {
     $(this).trigger('submit')

});
 $('#filter').on('apply.daterangepicker',function () {
     $(this).trigger('submit')

});
 $('#filter').on('change',function () {

     $(this).trigger('submit')

});
 $('.clear_button').on('click',function () {
    $('input').each(function () {
        $(this).val('')
    })
     // $(".select2-simple").select2("val", "");
        $(".select2-simple").val('').trigger('change')


     $("#filter").trigger('submit')

})