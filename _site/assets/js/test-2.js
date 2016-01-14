function refreshPrice(data) {
    var p = document.getElementById('test-jsonp');
    p.innerHTML = '当前城市：' +
        data['city'].name +': ' + 
        data['0000001'].price + '；' +
        data['1399001'].name + ': ' +
        data['1399001'].price;
}
function getPrice() {
    var
        js = document.createElement('script'),
        head = document.getElementsByTagName('head')[0];
	
    js.src = 'http://wthrcdn.etouch.cn/weather_mini?citykey=101010100';
    head.appendChild(js);
}