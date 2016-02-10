google.charts.load('current', {packages:['corechart', 'table', 'controls']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
	//Retrieve data from server in JSON format
	var jsonData = $.ajax({
		url: "/get_dashboard_sentiment",
		contentType:"application/json; charset=utf-8",
		dataType: "json",
		async: false
		}).responseJSON;
	
	var symbol = jsonData['result'][0]
	var security_name = jsonData['result'][1]
	var sector = jsonData['result'][2]
	var industry = jsonData['result'][3]
	var sentiment_volume = jsonData['result'][4]
	var recent_sentiment = jsonData['result'][5]
	
		
	//Create DataTable 
	var data = new google.visualization.DataTable();
	data.addColumn('string', 'Symbol');
    data.addColumn('string', 'Security Name');
	data.addColumn('string', 'Sector');
	data.addColumn('string', 'Industry');
	data.addColumn('number', 'Sentiment Volume');
	data.addColumn('number', 'Recent Sentiment');

	
	for (var i = 0; i < symbol.length; ++i) {
		var link = '<a href="/">' + symbol[i] + '</a>'
		data.addRow([link, security_name[i], sector[i], industry[i], recent_sentiment[i], sentiment_volume[i]]);
	}
	
	var dashboard = new google.visualization.Dashboard(
		document.getElementById('stringFilter_dashboard_div'));
		
    var control = new google.visualization.ControlWrapper({
		'controlType': 'StringFilter',
		'containerId': 'stringFilter_control_div',
		'options': {
			'filterColumnIndex': '0'
		}
	});
	
	var chart = new google.visualization.ChartWrapper({
		'chartType': 'Table',
		'containerId': 'stringFilter_chart_div',
		'options': {
			'height': '100%', 
			'width': '100%',
			'page': 'enable',
			'allowHtml': true}
	});
	
	dashboard.bind(control, chart);
    dashboard.draw(data);
	

	
};