$(function () {
	var sys = {};
	var ua = navigator.userAgent.toLowerCase();
	var s;
	(s = ua.match(/rv:([\d.]+)\) like gecko/)) ? sys.ie = s[1] :
	(s = ua.match(/msie ([\d.]+)/)) ? sys.ie = s[1] :
	(s = ua.match(/firefox\/([\d.]+)/)) ? sys.firefox = s[1] :
	(s = ua.match(/chrome\/([\d.]+)/)) ? sys.chrome = s[1] :
	(s = ua.match(/opera.([\d.]+)/)) ? sys.opera = s[1] :
	(s = ua.match(/version\/([\d.]+).*safari/)) ? sys.safari = s[1] : 0;

	if (!sys.firefox && !sys.chrome && !sys.safari) {
		$(".myborder2").css({border: '1px solid #e0e0e0'});
		$(".myborder2").css({padding: '10% 7% 10%'});
		$(".article_body").css({border: '1px solid #e0e0e0'});
		$(".article_body").css({padding: '70px 7% 50px'});
	}
});