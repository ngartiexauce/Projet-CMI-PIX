	var data_niv_1 = {{ niv_1|tojson }};
 	var data_niv_2 = {{ niv_2|tojson }};
 	var data_niv_3 = {{ niv_3|tojson }};
 	var data_niv_4 = {{ niv_4|tojson }};
 	var data_niv_5 = {{ niv_5|tojson }};

//functions for toggling between data
function change(value){

	if(value == '1'){
		update(data_niv_1);
	}else if(value =='2'){
		update(data_niv_2);
	}else if(value =='3'){
		update(data_niv_3);
	}else if(value =='4'){
		update(data_niv_4);
	}else{
		update(data_niv_5);
	}
}

function update(data){
	//set domain for the x axis
	xChart.domain(data.map(function(d){ return d.cle; }) );
	//set domain for y axis
	yChart.domain( [0, d3.max(data, function(d){ return +d.note; })] );
	
	//get the width of each bar 
	var barWidth = width / data.length;
	
	//select all bars on the graph, take them out, and exit the previous data set. 
	//then you can add/enter the new data set
	var bars = chart.selectAll(".bar")
					.remove()
					.exit()
					.data(data)		
	//now actually give each rectangle the corresponding data
	bars.enter()
		.append("rect")
		.attr("class", "bar")
		.attr("x", function(d, i){ return i * barWidth + 1 })
		.attr("y", function(d){ return yChart( d.note); })
		.attr("height", function(d){ return height - yChart(d.note); })
		.attr("width", barWidth - 1)
		.attr("fill", function(d){ 
			if(d.id === "pos"){
				return "rgb(251,180,174)";
			}else{
				return "rgb(179,205,227)";
			}
		});
	//left axis
	chart.select('.y')
		  .call(yAxis)
	//bottom axis
	chart.select('.xAxis')
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis)
		.selectAll("text")
			.style("text-anchor", "end")
			.attr("dx", "-.8em")
			.attr("dy", ".15em")
			.attr("transform", function(d){
				return "rotate(-65)";
			});
			
}//end updat

//set up chart
var margin = {top: 20, right: 20, bottom: 95, left: 50};
var width = 800;
var height = 500;

var chart = d3.select(".chart")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var xChart = d3.scaleBand()
				.range([0, width]);
				
var yChart = d3.scaleLinear()
				.range([height, 0]);

var xAxis = d3.axisBottom(xChart);
var yAxis = d3.axisLeft(yChart);


	chart.append("g")
		  .attr("class", "y axis")
		  .call(yAxis)
		  
	//bottom axis
	chart.append("g")
		.attr("class", "xAxis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis)
		.selectAll("text")
			.style("text-anchor", "end")
			.attr("dx", "-.8em")
			.attr("dy", ".15em")
			.attr("transform", function(d){
				return "rotate(-65)";
			});

//add labels
chart
	.append("text")
	.attr("transform", "translate(-35," +  (height+margin.bottom)/2 + ") rotate(-90)")
	.text("% des étudiants");
		
chart
	.append("text")
	.attr("transform", "translate(" + (width/2) + "," + (height + margin.bottom - 5) + ")")
	.text("Compétences");

//use bothData to begin with
update(data_niv_1);