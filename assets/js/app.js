$(function () {
    $("#sidebar").addClass("img-" + Math.round((Math.random() * 4 + 1)));

    if (window.location.href == "http://liticer.github.io/") {
        $("#sidebar").css({width: '100%'});
        $("#btnblog").click(function () {
            $("#sidebar").animate({width: '30%'}, 'slow');
        });
    }

    $('#article_body a').attr("target", "_blank");
});
