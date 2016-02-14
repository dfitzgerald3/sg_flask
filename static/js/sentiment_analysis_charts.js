google.charts.load('current', {packages: ['corechart', 'line', 'table', 'gauge','controls']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
	//google.charts.load('current', {packages: ['corechart', 'line', 'table', 'gauge','controls']});
	//Retrieve data from server in JSON format
	
	var url = window.location.href;
	var parser = document.createElement('a');
	parser.href = url;
	var pathname = parser.pathname;	
	
	var func = "/get_sentiment_sym/" + pathname.slice(20, pathname.lenth);
	
	//var url = "/get_sentiment_sym/" + sym;
	console.log(pathname)
	
	var jsonData = $.ajax({
		url: func,
		contentType:"application/json; charset=utf-8",
		dataType: "json",
		async: false
		}).responseJSON;
	
	console.log(jsonData)
	//Convert JSON data to useable arrays
	var db_data = [];
	for (var item in jsonData) {
		var value = jsonData[item];
		db_data.push(value);
	};
	
	console.log(db_data)
	
	var year = db_data[0][0]
	var month = db_data[0][1]
	var day = db_data[0][2]
	var open = db_data[0][3]
	var close = db_data[0][4]
	var high = db_data[0][5]
	var low = db_data[0][6]
	var sent = db_data[0][7]
	var sent_volume = db_data[0][8]
	
	console.log(year)
	
	//Create DataTable 
	var data = new google.visualization.DataTable();
	data.addColumn('date', 'Date');
    data.addColumn('number', 'Low');
	data.addColumn('number', 'Open');
	data.addColumn('number', 'Close');
	data.addColumn('number', 'High');
	data.addColumn('number', 'Sentiment');
	data.addColumn('number', 'Sentiment Volume');
	
	for (var i = 0; i < year.length; ++i) {
		var date = new Date(year[i], month[i], day[i]);
		data.addRow([date, low[i], open[i], close[i], high[i], sent[i], sent_volume[i]]);
	};
	
	
	//Create Dashboard
	var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));
	
	//Create ControlWrapper
	var control = new google.visualization.ControlWrapper({
		'controlType': 'ChartRangeFilter',
		'containerId': 'control_div',
		'options': {

			// Filter by the date axis.
			'filterColumnIndex': 0,
			'ui': {
				'chartType': 'LineChart',
				'chartOptions': {
					'chartArea': {
						'top': '0',
						'left': 115,
						'right': 115,
						'width': '80%',
						'height': '50%'
						},
					'hAxis': {
						'baselineColor': 'none',
						'title': 'Date',
							'gridlines': {
								//'count': 0
							}
						}
					},
				// Display a single series that shows the closing value of the stock.
				// Thus, this view has two columns: the date (axis) and the stock value (line series).
				'chartView': {
					'columns': [0, 3]
					},
				}
			},
		});
	
	
	// Create LineChart from Server Data
	var line_chart = new google.visualization.ChartWrapper({
		'chartType': 'LineChart',
		'containerId': 'line_div',
		'view': {'columns': [0, 5]},
		'options': {
			'width': '90%',
			'legend': {
				'position': 'none'
			}, 
			'hAxis': { 
				'textPosition': 'none',
				'gridlines': {
					'count': 0
				}
			},
			'vAxis': {
				'title': 'Sentiment',
				'maxValue': 1.0,
				'minValue': -1.0,
				'gridlines': {
					'count': 3
				}
			},
			'chartArea': {
				'top': '15',
				'bottom': '5'
			}
		}
	});
	
	
	// Create CandlestickChart from Server Data
	var cs_chart = new google.visualization.ChartWrapper({
		'chartType': 'CandlestickChart',
		'containerId': 'cs_div',
		'view': {'columns': [0, 1, 2, 3, 4]},
		'options': {
			'width': '90%',
			'legend': {
				'position': 'none'
			}, 
			'hAxis': { 
				'textPosition': 'none',
				'gridlines': {
					'count': 0
				}
			},
			'vAxis': {
				'title': 'Stock Price',
				'gridlines': {
					'count': 3
				}
			},
			'chartArea': {
				'top': 15,
				'bottom': 5
			}
		}
	});
	
	
	// Create BarChart from Server Data
	var bar_chart = new google.visualization.ChartWrapper({
		'chartType': 'ColumnChart',
		'containerId': 'bar_div',
		'view': {'columns': [0, 6]},
		'options': {
			'width': '90%',
			'legend': {
				'position': 'none'
			}, 
			'hAxis': { 
				'textPosition': 'none',
				'gridlines': {
					'count': 0
				}
			},
			'vAxis': {
				'title': 'Sentiment Volumne',
				'gridlines': {
					'count': 3
				}
			},
			'chartArea': {
				'top': 5,
				'bottom': 5
			}
		}
	});
	
		
	dashboard.bind(control, [line_chart, cs_chart, bar_chart]);
	dashboard.draw(data);
}