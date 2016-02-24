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
		
	var jsonData = $.ajax({
		url: func,
		contentType:"application/json; charset=utf-8",
		dataType: "json",
		async: false
		}).responseJSON;
	
	//Convert JSON data to useable arrays
	var db_data = [];
	for (var item in jsonData) {
		var value = jsonData[item];
		db_data.push(value);
	};
	
		
	var year = db_data[0][0]
	var month = db_data[0][1]
	var day = db_data[0][2]
	var open = db_data[0][3]
	var close = db_data[0][4]
	var high = db_data[0][5]
	var low = db_data[0][6]
	var sent = db_data[0][7]
	var sent_volume = db_data[0][8]
	
		
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
		var date = new Date(year[i], (month[i] - 1), day[i]);
		data.addRow([date, low[i], open[i], close[i], high[i], sent[i], sent_volume[i]]);
	};
	
	
	//Create Dashboard
	var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));
	
	//Create ControlWrapper
	control = new google.visualization.ControlWrapper({
		'controlType': 'ChartRangeFilter',
		'containerId': 'control_div',
		'options': {

			// Filter by the date axis.
			'filterColumnIndex': 0,
			'ui': {
				'chartType': 'LineChart',
				'chartOptions': {
					'colors': ['2D7187'],
					'chartArea': {
						'top': '0',
						'width': '75%',
						'height': '50%'
						},
					'hAxis': {
						'baselineColor': 'none',
						'title': 'Date'
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
			'colors': ['2D7187'],
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
				'maxValue': 0.1,
				'minValue': -0.1,
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
			'colors': ['2D7187', '2D7187'],
			'legend': {
				'position': 'none'
			}, 
			'candlestick': {
				'fallingColor': {
					'stroke': '2D7187',
				},
				'risingColor': {
					'stroke': '2D7187',
					'fill': '2D7187'
				}
			},
			'hAxis': { 
				'textPosition': 'none',
				'gridlines': {
					'count': 0
				}
			},
			'vAxis': {
				'title': 'Stock Price',
				'format': 'currency',
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
			'colors': ['2D7187'],
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
				'top': 15,
				'bottom': 5,
				'width': '75%'
			}
		}
	});
	
		
	dashboard.bind(control, [line_chart, cs_chart, bar_chart]);
	
	dashboard.draw(data);
	
};

function changeRange(value) {
			var min = new Date();				
			min.setDate(min.getDate() - value);

			var today = new Date();
			console.log(min)
			console.log(today)
			
			control.setState({range:{
				start: min,
				end: today
				}
			});
			console.log(control.getState());
			control.draw();
		};

