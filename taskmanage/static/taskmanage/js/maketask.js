$(function(){
    $('.col').sortable();

    $('#add_entry').click(function(){
        var adding = '<div class="input-group p-0 pb-2 mb-2"><span class="input-group-text"><i class="bi bi-chevron-expand"></i></span><input type="text" class="form-control" placeholder="項目を入力して下さい" name="checks"><div class="delete_entry"><button type="button" class="btn btn-outline-secondary"><i class="bi bi-dash"></i></button></div></div>';
        $('.col').append(adding);
    });
    $(document).on('click', '.delete_entry', function() {
        $(this).parents('.input-group').remove();
    });
});

document.addEventListener('DOMContentLoaded', function() {

    flatpickr.l10ns.ja.firstDayOfWeek = 0;  

    flatpickr('#datetimepicker', {
        wrap : true,
        enableTime : true,
        dateFormat : 'Y/m/d H:i',
        defaultHour : 23,
        defaultMinute : 59,
        hourIncrement : 1,
        minuteIncrement : 5,
        locale : 'ja',
        clickOpens : true,
        allowInput : true,
    });
});