$(document).ready(function () {
    $(".hamburger").click(function () {
        $(this).toggleClass("is-active");
        $('.mobile-lnb').toggleClass("is-display");
    });

});