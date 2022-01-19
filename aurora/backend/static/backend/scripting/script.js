$(function() {


    $('.sidebar-nav').find('.has-dropdown').click(function(event){
        event.preventDefault();
        var current_dropdown = $(this).parent().find('.sidebar-dropdown');
        $('.sidebar-dropdown').animate({'height': 'hide'}, 175);
        if (current_dropdown.is(':hidden')) {
            current_dropdown.animate({'height': 'show'}, 175);
        }
    })

    // change Django filename to make it shorter
    $('a[href*="media/"]').each(function(index, element) {
        if (! $(this).attr('class')) {
            var filepath = $(element).text();
            var fp_split = filepath.split("/");
            var filename = fp_split[fp_split.length - 1]
            $(element).text(filename);
        }
    })

})
