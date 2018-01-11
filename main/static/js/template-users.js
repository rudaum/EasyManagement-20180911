$(document).ready(function(){
    var urlarray = window.location.href.split('/');
    if (urlarray.length == 5) {
        var user = urlarray[urlarray.length - 1];
        $('#' + user).show();
        window.history.pushState('page2', 'Title', '/users');
    }
    $("#userFilter").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".dropdown-menu li").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    $('.dropdown-menu li').click(function () {
        if (user != '') {
            $('#' + user).hide();
            user = '';
        };
    });
});