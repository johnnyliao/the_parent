/*
 * DIV高度自動延展100%
 * 適用瀏覽器：IE8.0+、Firefox3.6+、Chrome10+、Safari5.0
 * 初版:飛肯-姜智豪老師       http://www.flycan.com.tw
 * 二版:飛肯-男丁老師         http://abgne.tw
 * 三版:飛肯-男丁老師&梅問題  http://www.minwt.com
 */
$(window).load(function () {
    var b = $('[_height=auto]');
    if (b.length <= 0) return false;
    var c = $(this),
        $body = $('body'),
        $none = $('[none=true]'),
        autoDivHeight = b.outerHeight(true),
        autoDivBorder = autoDivHeight - b.height(),
        delBodyMargin = parseInt($body.css('marginTop')) + parseInt($body.css('marginBottom')),
        none = $none.outerHeight(true) - $none.height(),
        delHeight = 0;
    $('[_height=none]').each(function () {
        delHeight += $(this).outerHeight(true)+9
    });

    function fullHeight() {
        var a = c.height() - delHeight - delBodyMargin - autoDivBorder - none;
        if (a > autoDivHeight) {
            b.height(a)
        }
    }
    c.resize(function () {
        fullHeight()
    });
    fullHeight()
});