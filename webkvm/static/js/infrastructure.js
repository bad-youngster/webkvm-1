$.expr[':'].Contains = $.expr.createPseudo(function (arg) {
    return function (elem) {
        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});

$(document).ready(function () {
    // event button labled
    $('#filter_button').click(function (event) {
        //get value
        var filter_val = $('#fileter_input').val();
        if (filter_val === '') {
            // show all
            $('tbody tr').show();
        } else {
            // show only matches
            $('tbody tr:Contanis(\'' + filter_val + '\')').show();
            // not-matches items
            $('tbody tr:not(:Contains(\'' + filter_val + '\'))').hide();

        }
    });
   // event button labeled clear
   $('#filter_clear').click(function (event) {
       $('#filter_input').val('');
       $('#filter_button').click();
   });
   //filter when enter key pressed
    $('#filter_input').keyup(function (event) {
        if (event.keyCode === 13){
            $('#filter_button').click();

        }
    });
    $('#hide_vms_bystate input[type=checkbox]').change(function () {
        $('tbody tr[data-status=' + $(this).data('value') + ']').toggle();
    });
});