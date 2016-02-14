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
	
	//Assign data to individual arrays
	var symbol = jsonData['result'][0]
	var security_name = jsonData['result'][1]
	var sector = jsonData['result'][2]
	var industry = jsonData['result'][3]
	var recent_sentiment = jsonData['result'][4] 
	var sentiment_volume = jsonData['result'][5]
	
	//Convert Recent Sentiment to INT so that the slider will work
	var recent_sentiment_int = [];
	for (var i =0; i < recent_sentiment.length; ++i) {
		recent_sentiment_int.push(Math.round(recent_sentiment[i] * 100));
	};
	
		
	//Create DataTable 
	var data = new google.visualization.DataTable();
	data.addColumn('string', 'Symbol');
    data.addColumn('string', 'Security Name');
	data.addColumn('string', 'Sector');
	data.addColumn('string', 'Industry');
	data.addColumn('number', 'Sentiment Volume');
	data.addColumn('number', 'Recent Sentiment');

	
	//Assign values to DataTable
	for (var i = 0; i < symbol.length; ++i) {
		var link = '<a href="/sentiment_analysis/' + symbol[i] + '">' + symbol[i] + '</a>'
		data.addRow([link, security_name[i], sector[i], industry[i], sentiment_volume[i], recent_sentiment_int[i]]);
	}
	
	
	//Create Google Charts Dashboard
	var dashboard = new google.visualization.Dashboard(
		document.getElementById('stringFilter_dashboard_div'));
	

	//Create a String Filter that will filter the Security Name
    var stringfilter = new google.visualization.ControlWrapper({
		'controlType': 'StringFilter',
		'containerId': 'stringFilter_control_div',
		'options': {
			'filterColumnIndex': '1',
			'ui': {
				'labelStacking': 'vertical'
			}
		}
	});
	
	
	//Create a Category Filter that will filter the sector category
	var categoryfilter = new google.visualization.ControlWrapper({
		'controlType': 'CategoryFilter',
		'containerId': 'categoryFilter_dashboard_div',
		'options': {
			'filterColumnIndex': 2,
			'ui': {
				'allowtyping': false,
				'allowMultiple': true,
				'selectedValuesLayout': 'belowStacked',
				'labelStacking': 'vertical',
				'cssClass': 'dropdown'
			}
		},
		//'state': {'selectedValues': ['Consumer Discretionary', 'Consumer Staples', 'Energy', 'Financials', 'Health Care', 'Industrials', 'Information Technology', 'Materials', 'Telecommunications Services', 'Utilities']}
		
	});
	
	
	
	//Create a Number Range Filter that will filter the Sentiment Volume
	//Make the upper range of the filter round to the nearest thousand
	var max_filter_vol = Math.ceil(Math.max.apply(Math, sentiment_volume) / 1000) * 1000;
	
	var sentvolfilter = new google.visualization.ControlWrapper({
		'controlType': 'NumberRangeFilter',
		'containerId': 'sentVolFilter_dashboard_div',
		'options': {
			'filterColumnIndex': 4,
			'minValue': 1,
			'maxValue': max_filter_vol,
			'ui': {
				'labelStacking': 'vertical'
			}
		}
	});
	
	
	
	//Create a Number Range Filter for the Recent Sentiment value
	var sentfilter = new google.visualization.ControlWrapper({
		'controlType': 'NumberRangeFilter',
		'containerId': 'sentFilter_dashboard_div',
		'options': {
			'filterColumnIndex': 5,
			'minValue': -100.0,
			'maxValue': 100.0,
			'ui': {
				'labelStacking': 'vertical',
				'step': 1
			}
		}
	});
	
	
	//Create a Table to house all of the data
	var chart = new google.visualization.ChartWrapper({
		'chartType': 'Table',
		'containerId': 'stringFilter_chart_div',
		'options': {
			'width': '100%',
			'page': true,
			'pageSize': 25,
			'allowHtml': true
		}
	});
	
	dashboard.bind([stringfilter, categoryfilter, sentvolfilter, sentfilter], chart);
    dashboard.draw(data);
	

	
};