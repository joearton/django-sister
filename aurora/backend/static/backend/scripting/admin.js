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

$(document).ready(function() {
    // {{ app_scripts }}
    var backend_ajax_url = "/administrator/backend/configuration/ajax";

    $('.ajax-handler').click(function(e){
        var elem = $(this);
        elem.prop('disabled', true);
        var name = $(this).attr('name');
        var value  = $(this).val();
        var callback  = $(this).attr('data-call');

        // if value is checkbox
        if ($(this).attr('type') == 'checkbox') {
            if ($(this).is(':checked')) {
                value = true;
            } else {
                value = "";
            }
        }

        var data = {'name': name, 'value': value};
        $.each(this.attributes, function(index, element) {
            if (element.name.startsWith('data-')) {
                var name = element.name.replace('data-', '');
                data[name] = element.value;
            }
        })

        $.ajax(backend_ajax_url, {
            type: 'POST',
            data: data,
            success: function(response, status, xhr) {
                window[callback](elem, response);
            },
            error: function(jqXhr, textStatus, errorMessage) {},
            complete: function(jqXhr, textStatus) {
                elem.prop('disabled', false);
            }
        })
    })

    
    var menu_sys = $('.main-sidebar').find('a[href$="backend/configuration/system"]');
    var check_sys_problems = function() {
        $.ajax(backend_ajax_url, {
            type: 'POST',
            data: {page: 'system-config', 'name': 'get_sys_problems'},
            success: function(response, status, xhr) {
                if (response.data == false) {
                    menu_sys.addClass('bg-warning text-white');
                } else {
                    if (menu_sys.hasClass('bg-warning')) {
                        menu_sys.removeClass('bg-warning text-white');
                    }
                }
            },
        })
    }

    if (menu_sys) {
        check_sys_problems();
        setInterval(check_sys_problems, 5000);
    }

})
