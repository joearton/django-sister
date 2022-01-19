String.prototype.format = function() {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k])
    }
    return a
}

// Using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function ToCurrency(digits){
    var currency = '';		
    var digitrev = digits.toString().split('').reverse().join('');
    for(var i = 0; i < digitrev.length; i++) if(i%3 == 0) currency += digitrev.substr(i,3)+'.';
    return currency.split('', currency.length-1).reverse().join('');
}

function ToDigit(currency) {
    return parseInt(currency.replace(/,.*|[^0-9]/g, ''), 10);
}


$(function() {

    $(".phonenumber, .numberonly, .mobile_number").text(function(i, text) {
        if (text.length == 12) {
            text = text.replace(/(\d\d\d\d)(\d\d\d\d)(\d\d\d\d)/, "$1-$2-$3");
        } else if (text.length == 13) {
            text = text.replace(/(\d\d\d\d\d)(\d\d\d\d)(\d\d\d\d)/, "$1-$2-$3");
        } else {
            text = text.replace(/(\d\d\d\d)(\d\d\d)(\d\d\d\d)/, "$1-$2-$3");
        }
        return text;
    });

    
    $('.currency').text(function(index, text){
        text = ToCurrency(text);
        return text;
    });


    if ($(".dateinput, .datetimeinput").length) {
        var oggi = new Date();
        var year = oggi.getFullYear();
        $.datetimepicker.setLocale(language_code);
        var date_format = 'Y-m-d';
        if (language_code == 'id') {
            date_format = 'd-m-Y';
        }
        $(".dateinput, .datetimeinput").datetimepicker({
            timepicker: false,
            format: date_format,
            // minDate: (year-1) + '/01/01',
            // maxDate: (year+3) + '/12/31'
        });
    }


    if ($('input.timeinput').length) {
        $.datetimepicker.setLocale('id');
        $('input.timeinput').datetimepicker({
            datepicker: false,
            format: 'H:i',
            step:30,
        });
    }


    // only accept number input
    var number_selector = "input[name^='mobile_number'], input.only-accept-number, input[name^='nik_'], input[name='nik']";
    $(number_selector).on('input blur paste', function() {
        $(this).val($(this).val().replace(/\D/g, ''))
    })


    if ($('.messages').length) {
        $('.messages').hide().animate({'height': 'show'}, 500);
        setTimeout(function(){
            $('.messages').animate({'height': 'hide'}, 500);
        }, 7000);
    }


    $('.dialog-btn').click(function(event) {
        event.preventDefault();
        var width = '55%';
        var dialog_window = $('.dialog-window');
        dialog_window.dialog({
            modal: true,
            width: width,
        })
    })

    $('.messages').find('li').click(function(event){
        event.preventDefault();
        $(this).fadeOut(250);
    })


    // mengubah filename upload django
    if ($('.form-control.d-flex')) {
        $('.form-control.d-flex').find('a').each(function(index, element) {
            var label = $(element).text().split('/');
            $(element).text(label[label.length - 1]);
        })
    }


    // make responsive table
    $('.table').each(function(index, table){
        var table_responsive = $('<div/>', {'class': 'table-responsive'})
		$(table).parent().append(table_responsive);
        $(table).appendTo(table_responsive);
   
    })


});
