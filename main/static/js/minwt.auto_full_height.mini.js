/*
 * DIV���צ۰ʩ��i100%
 * �A���s�����GIE8.0+�BFirefox3.6+�BChrome10+�BSafari5.0
 * �쪩:����-�������Ѯv       http://www.flycan.com.tw
 * �G��:����-�k�B�Ѯv         http://abgne.tw
 * �T��:����-�k�B�Ѯv&�����D  http://www.minwt.com
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