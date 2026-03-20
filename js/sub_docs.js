$(window).scroll(function () {
    if ($(this).scrollTop() >= 100) {
        $('.lnb').css('position', 'fixed');
        $('.lnb').css('top', '0px');
    } else {
        $('.lnb').css('position', 'absolute');
        $('.lnb').css('top', '100px');
    }
});