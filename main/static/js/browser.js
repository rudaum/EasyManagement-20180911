$(function () {
    $('ul.tree').hide();
    $('label.tree-toggler').click(function () {
        $(this).parent().children('ul.tree').toggle(600);
        if ($(this).html().includes("+")) {
            $(this).html($(this).html().replace("+","-"));
        } else if ($(this).html().includes("-")) {
            $(this).html($(this).html().replace("-","+"));
        }
    });

    $('#tree-toggler').click(function () {
        if ($(this).html().includes("+")) {
            $('ul.tree').show(600);
            $(this).html($(this).html().replace("+","-"));
            $('label.tree-toggler').each(function() {
                $(this).html($(this).html().replace("+","-"))
            });
        } else if ($(this).html().includes("-")) {
            $('ul.tree').hide(600);
            $(this).html($(this).html().replace("-","+"));
            $('label.tree-toggler').each(function() {
                $(this).html($(this).html().replace("-","+"))
            });
        }
    });
});