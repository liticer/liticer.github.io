function weather(){
	var yqlUrl3= "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%3D26198119%20and%20u%3D%22c%22&format=json&diagnostics=true&callback=";
    $.getJSON(yqlUrl3, function(data){
		//$('#test-jsonp>p').remove();

		var allTexts = JSON.stringify(data.query.results.channel.item.description);

		var re = /<img\ src=\\"(.*?)\\/;
		var imgsrc = re.exec(allTexts);
		
		var re2 = /<b>(.*?)<\/b><br\ \/>\\n(.*?)<BR\ \/>/;
		var imgsrc2 = re2.exec(allTexts);
		
		var re3 = /<b>Forecast:.*?\\n(.*?)</;
		var imgsrc3 = re3.exec(allTexts);
		
		$('#test-jsonp').append($('<p/>').html('<img src="' + imgsrc[1] + '"/>' + " " + imgsrc2[2] + ". " + imgsrc3[1]));
		
		
		//$('#test-jsonp').append($('<p/>').html(data.query.results.channel.item.description));

	});
}