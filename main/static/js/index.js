$(function () {
        $('ul.tree').hide();
        $('label.tree-toggler').click(function () {
            $(this).parent().children('ul.tree').toggle(600);
            if ($(this).text().includes("+")) {
                $(this).text($(this).text().replace("+","-"));
            } else if ($(this).text().includes("-")) {
                $(this).text($(this).text().replace("-","+"));
            }
        });
    });