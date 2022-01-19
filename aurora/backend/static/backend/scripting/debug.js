// reload browser automatically for development purpose

setInterval(function() {
    var data = {
        debug: 'auto_reload',
    }
    $.post(base_url + '/backend/debug/auto_reload', data=data, function(data){
        if (data.auto_reload) {
            console.log("Reload browser automatically...")
            window.location.reload();
        }
    });
}, 750);
