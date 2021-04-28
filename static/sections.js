var scrollVis = function () {
    // constants to define the size
    // and margins of the vis area.
    var width = 600;
    var height = 520;
    var margin = { top: 0, left: 20, bottom: 40, right: 10 };
  
    // Keep track of which visualization
    // we are on and which was the last
    // index activated. When user scrolls
    // quickly, we want to call all the
    // activate functions that they pass.
    var lastIndex = -1;
    var activeIndex = 0;

    // When scrolling to a new section
  // the activation function for that
  // section is called.
    var activateFunctions = [];
    setupSections()
    var setupSections = function () {
        // activateFunctions are called each
        // time the active section changes
        activateFunctions[0] = welcome;
        activateFunctions[1] = about;
        activateFunctions[2] = showMap;
        activateFunctions[3] = showChart;
        activateFunctions[4] = future;
        activateFunctions[5] = thankYou;

    }     
    //beginning of showMap function
    var width = 960;
    var height = 500;
    
    // D3 Projection
    var projection = d3.geoAlbersUsa()
        .translate([width / 2, height / 2])    // translate to center of screen
        .scale([1000]);          // scale things down so see entire US
    
    // Define path generator
    var path = d3.geoPath()               // path generator that will convert GeoJSON to SVG paths
        .projection(projection);  // tell path generator to use albersUsa projection
    
    
    // Define linear scale for output
    var color = d3.scaleLinear()
        .range(["#fafa6e", "#c4ec74", "#92dc7e", "#64c987", "#39b48e", "#089f8f", "#00898a", "#08737f", "#215d6e", "#2a4858"])
        .domain([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    
    var legendText = ["91+ decile", "81-90 perecentile", "71-80 decile", "61-70 decile", "51-60 decile",
        "41-50 decile", "31-40 decile", "21-30 decile", "11-20 decile", "1-10 decile"];
    var mapDiv =d3.select("body")
        .append("div")
        .attr("class", "mapDiv")
        .attr("width", "100%")
        .attr("height", "100%")
        .style("align", "center");
    //Create SVG element and append map to the SVG
    var svg = d3.select(".mapDiv")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("position", "absolute");
    
    
    
    
    // Append Div for tooltip to SVG
    var div = d3.select(".mapDiv")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
    
    var displayYear = d3.select(".mapDiv")
        .append("div")
        .attr("class", "displayYear")
        .style("color", "#2a4858")
        .style("font-size", "30px")
    
    
    
    
    
    var years = [2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011]
    var copyYears = []
    
    Object.assign(copyYears, years)
    
    var mapInterval = setInterval(function () {
        if (years.length > 0) {
            renderMap(years.pop())
        }
    }, 1000)
    
    var restartButton = d3.select(".mapDiv")
        .append("button")
        .text("Restart")
        .attr("class", "restart")
        .style("opacity", 0)
        .style("align", "right")
        .style("color", "#FFFFFF")
        .style("background-color", "#2a4858")
        .style("border-radius", "10px")
        .on("mouseover", function (d) {
            restartButton.style("color", "#2a4858")
                .style("background-color", "#FFFFFF")
        })
        .on("mouseout", function (d) {
            restartButton.transition()
                .duration(200)
                .style("color", "#FFFFFF")
                .style("background-color", "#2a4858")
        })
        .on("click", function () {
            Object.assign(years, copyYears)
            restartButton.style("opacity", 0)
            mapInterval = setInterval(function () {
                if (years.length > 0) {
                    renderMap(years.pop())
                }
            }, 1000)
        })
    
    
    
    function renderMap(year) {
    
    
        d3.json(`/load-data/${year}`).then(function (state_data) {
            console.log(year)
            if (years.length == 0) {
                console.log("CLEAR")
                clearInterval(mapInterval)
                restartButton.style("opacity", 1)
                console.log("BUTTON")
    
            }
            d3.json("/us-states.json").then(function (states_json) {
    
    
    
                // Loop through each state data value in the .csv file
                for (var i of state_data) {
    
                    // Grab State ID
                    var dataStateID = i[0]
    
                    // Grab State Name
                    var dataState = i[2]
    
                    // Grab decile value 
                    var dataValue = i[4]
    
                    // Grab data year
                    var dataYear = i[5]
    
                    // Grab count per 100,000
                    var dataCount = i[3]
    
                    //***send all data to the front
    
    
                    // Find the corresponding state inside the GeoJSON
                    for (var j = 0; j < states_json.features.length; j++) {
                        var jsonState = states_json.features[j].properties.name;
    
                        if (dataState == jsonState) {
    
                            // Copy the data value into the JSON
                            //has only a key 'name'
                            states_json.features[j].properties.decile = dataValue
                            states_json.features[j].properties.count = dataCount
                            // Stop looking through the JSON
    
                            break;
                        }
                    }
                }
                function handleClick(path) {
                    var state = path.properties.name
                    window.location.href = `/state/${state}`;
                }
    
                displayYear.join(
                    enter => enter.append("p")
                        .text(`${year}`),
                    update => update.text(`${year}`)
                )
    
                // // Bind the data to the SVG and create one path per GeoJSON feature
                svg.selectAll("path")
                    .data(states_json.features)
                    .join(
                        enter => enter.append("path")
                            .attr("d", path)
                            .attr("id", "hover-text")
                            .style("stroke", "#fff")
                            .style("stroke-width", "1")
                            .style("fill", function (f) {
    
                                // Get data value
    
                                var decile = f.properties.decile;
    
                                if (decile) {
                                    //If value exists…
                                    return color(decile);
                                }
                            }),
                        update => update.style("fill", function (f) {
    
                            // Get data value
    
                            var decile = f.properties.decile;
                            if (decile) {
                                //If value exists…
                                return color(decile);
                            }
                        })
                    )
                    .on("click", handleClick)
                    .on("mouseover", function (d) {
                        var state = d.properties.name
                        var count = d.properties.count
                        div.transition()
                            .duration(200)
                            .style("opacity", .9);
                        div.html(state + "<br/>" + count)
                            .style("left", (d3.event.pageX) + "px")
                            .style("top", (d3.event.pageY - 28) + "px")
                    })
                    .on("mouseout", function (d) {
                        div.transition()
                            .duration(500)
                            .style("opacity", 0);
                    });
            });
    
        });
    
    }
    
    
    
    // Modified Legend Code from Mike Bostock: http://bl.ocks.org/mbostock/3888852
    var legend = d3.select(".mapDiv").append("svg")
        .attr("class", "legend")
        .attr("width", 140)
        .attr("height", 200)
        .selectAll("g")
        .data(color.domain().slice().reverse())
        .enter()
        .append("g")
        .attr("transform", function (d, i) { return "translate(0," + i * 20 + ")"; });
    
    legend.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);
    
    legend.append("text")
        .data(legendText)
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .text(function (d) { return d; });

    // Modified Legend Code from Mike Bostock: http://bl.ocks.org/mbostock/3888852
    var legend = d3.select("body").append("svg")
        .attr("class", "legend")
        .attr("width", 140)
        .attr("height", 200)
        .selectAll("g")
        .data(color.domain().slice().reverse())
        .enter()
        .append("g")
        .attr("transform", function (d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .data(legendText)
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .text(function (d) { return d; });
    }
    //end of showMap function

    //beginning of showChart function
    f

    var state = document.getElementById("load-state").getAttribute("value");
    
    renderChart(state)
    
    function renderChart(state){	
        
        function updateData(state) {
            d3.select("#load-state").html(`${state}`)
            d3.csv(`/load-state-data/${state}`).then(d => chart(d))
        };
        d3.csv(`/load-state-data/${state}`).then(d => chart(d))
        function chart(data) {   // a function called chart
            // data.sort(function (a,b) {return d3.ascending(a.date, b.date);});
            console.log(data)
            var keys = data.columns.slice(1); // creates a variable called keys sets the value to the header after beginning with the second element
        
            var parseTime = d3.timeParse("%Y"), // creates variables for methods for handling dates
                formatDate = d3.timeFormat("%Y"),
                bisectDate = d3.bisector(d => d.date).left,
                formatValue = d3.format(",.0f");
        
            data.forEach(function(d) { // walks through the data and calls parseTime on all dates
                d.date = parseTime(d.date); // d.date *note 'date' comes from the csv header
                return d;
            })
        
            var svg = d3.select("#chart"),  // creates a variable pertaining to the svg including one called svg and assigns it to the svg element with the id 'chart'
                margin = {top: 15, right: 35, bottom: 15, left: 55}, // creates variable margin and assigns a dictionary of parameters
                width = +svg.attr("width") - margin.left - margin.right, // creates variable width and assigns the attribute width from the html element and subtracts the left and right margins
                height = +svg.attr("height") - margin.top - margin.bottom; // creates variable height and assigns the attribute height from the html element and subtracts the top and bottom margins
        
            var x = d3.scaleTime() // creates the variable x and assigns it the d3 scaleTime method
                .rangeRound([margin.left, width - margin.right]) // makes round numbers
                .domain(d3.extent(data, d => d.date)) // returns an array of the minimum and maximum values in the date column and set them as the domain of the x variable
        
            var y = d3.scaleLinear() // creates variable y and assigns it the function scaleLinear which will map values in a given range
                .rangeRound([height - margin.bottom, margin.top]); // rounds the numbers in the range
                
            var z = d3.scaleOrdinal(d3.schemeSet1);  // creates variable z and assigns it to a d3 ordinal scale taking the built in color scheme, schemeCategory10
        
            var line = d3.line() // creates variable line an assigns it the function d3.line which creates a line out of sequenced points
                .curve(d3.curveCardinal) // assigns the attribute curve to the line using ing d3's built in curveCardinal curve generator
                .x(d => x(d.date)) // assigns the date to the x axis
                .y(d => y(d.counts)); // assigns the counts to the y axis
        
            svg.append("g") // establishes a group element for the svg
                .attr("class","x-axis") // assigns x-axis as the class for this element
                .attr("transform", "translate(0," + (height - margin.bottom) + ")") // tells the svg where to render on the x axis
                .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%Y"))); // creates the bottom axis calling the x variable and uses the time data for the bottom ticks
            svg.append("g") // establishes another group element for the svg
                .attr("class", "y-axis") // assigns the y-axis as the class
                .attr("transform", "translate(" + margin.left + ",0)"); // tell the svg where to render on the y axis
        
            var focus = svg.append("g") // establishes a variable focusand assigns it to the svg group as an element
                .attr("class", "focus") // assigns focus as the class
                .style("display", "none"); // tells it not to display
        
            focus.append("line").attr("class", "lineHover") // appends a line element to the focus object and assigns it the class lineHover
                .style("stroke", "#999") // assigns the color of the line
                .attr("stroke-width", 1) // assigns the widths
                .style("shape-rendering", "crispEdges") // specifies that the line should be rendered with CSS builtin crispEdges
                .style("opacity", 0.5) // sets the opacity of the line to .5
                .attr("y1", -height) // sets the height of the line to the height of the y axis
                .attr("y2",0); // sets the bottom beginning of the line to 0
        
            focus.append("text").attr("class", "lineHoverDate") // appends a text elemnet to focus and assigns it the class "lineHoverDate"
                .attr("text-anchor", "middle") // tells the text element to align in the middle of the line 
                .attr("font-size", 12); // sets the font size of the text element
        
            var overlay = svg.append("rect") // creates variable overlay which is assigned to a builtin d3 shape rect being appended to the svg
                .attr("class", "overlay") // assigns class overlay
                .attr("x", margin.left) // establishes the range of the overlay on the x axis
                .attr("width", width - margin.right - margin.left) // sets the width of the overlay as a range from margin to margin on the x axis
                .attr("height", height) // sets the height to the value of the height variable
        
            update(d3.select('#selectbox').property('value'), 0); // calls the update function passing the value from the element with the id #selectbox
    
            function update(input, speed) {
                          
                var copy = keys.filter(f => f.includes(input)) // establishes a variable called copy and assigns it to the keys filtered by the includes method using the value input from the #selectbox element
        
                var data_types = copy.map(function(id) { // establishes a variable called data_types and assigns it to 
                    
                    return {
                        id: id,
                        values: data.map(d => {return {date: d.date, counts: +d[id]}})
                    };
                });
                var min = d3.min(data_types, d => d3.min(d.values, c => c.counts))
                var max = d3.max(data_types, d => d3.max(d.values, c => c.counts))
                y.domain([min, max])
                     .nice();
        
                svg.selectAll(".y-axis").transition()
                    .duration(speed)
                    .call(d3.axisLeft(y).tickSize(-width + margin.right + margin.left))
        
                var data_type = svg.selectAll(".data_types")
                    .data(data_types);
        
                data_type.exit().remove(); // It removes the data from the function that plots and draws the line,
                                                // before adding the new data
                data_type.enter().insert("g", ".focus").append("path")
                    .attr("class", "line data_types")
                    .style("stroke", d => z(d.id))
                    .merge(data_type)
                    .transition().duration(speed)
                    .attr("d", d => line(d.values))
        
                tooltip(copy);
            }
        
            function tooltip(copy) {
        
                var labels = focus.selectAll(".lineHoverText")
                    .data(copy)
        
                labels.exit().remove() 
            
                labels.enter().append("text")
                    .attr("class", "lineHoverText")
                    .style("fill", d => z(d))
                    .attr("text-anchor", "start")
                    .attr("font-size",12)
                    .attr("dy", (_, i) => 1 + i * 2 + "em")
                    .merge(labels);
        
                var circles = focus.selectAll(".hoverCircle")
                    .data(copy)
        
                circles.enter().append("circle")
                    .attr("class", "hoverCircle")
                    .style("fill", d => z(d))
                    .attr("r", 2.5)
                    .merge(circles);
        
                svg.selectAll(".overlay")
                    .on("mouseover", function() { focus.style("display", null); })
                    .on("mouseout", function() { focus.style("display", "none"); })
                    .on("mousemove", mousemove);
        
                function mousemove() {
        
                    var x0 = x.invert(d3.mouse(this)[0]),
                        i = bisectDate(data, x0, 1),
                        d0 = data[i - 1],
                        d1 = data[i],
                        d = x0 - d0.date > d1.date - x0 ? d1 : d0;
        
                    focus.select(".lineHover")
                        .attr("transform", "translate(" + x(d.date) + "," + height + ")");
        
                    focus.select(".lineHoverDate")
                        .attr("transform", 
                            "translate(" + x(d.date) + "," + (height + margin.bottom) + ")")
                        .text(formatDate(d.date));
        
                    focus.selectAll(".hoverCircle")
                        .attr("cy", e => y(d[e]))
                        .attr("cx", x(d.date));
        
                    focus.selectAll(".lineHoverText")
                        .attr("transform", 
                            "translate(" + (x(d.date)) + "," + height / 2.5 + ")")
                        .text(e => e + " " + formatValue(d[e]));
        
                    x(d.date) > (width - width / 4) 
                        ? focus.selectAll("text.lineHoverText")
                            .attr("text-anchor", "end")
                            .attr("dx", -10)
                        : focus.selectAll("text.lineHoverText")
                            .attr("text-anchor", "start")
                            .attr("dx", 10)
                }
            }
        
            var selectbox = d3.select("#selectbox")
                .on("change", function() {
                    update(this.value, 750);
                })
            var stateSelector = d3.select("#state-selector")
                .on("change", function() {
                    updateData(this.value);
                })
    
            
        }
    };
    
    //end of showChart function
}

function display(data) {
    // create a new plot and
    // display it
    var plot = scrollVis();
    d3.select('#vis')
        .datum(data)
        .call(plot);
    
    // setup scroll functionality
    var scroll = scroller()
        .container(d3.select('#graphic'));
    
    // pass in .step selection as the steps
    scroll(d3.selectAll('.step'));
    
    // setup event handling
    scroll.on('active', function (index) {
        // highlight current step text
        d3.selectAll('.step')
        .style('opacity', function (d, i) { return i === index ? 1 : 0.1; });
    
        // activate current section
        plot.activate(index);
    });
    
    scroll.on('progress', function (index, progress) {
        plot.update(index, progress);
    });
}