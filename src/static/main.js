
margin = ({top: 10, right: 40, bottom: 60, left: 30})
height = 500 + margin.top + margin.bottom
width = 800 + margin.left + margin.right

data = d3.csv("http://127.0.0.1:8000/data")
    .then(data => {
        const svg = d3
            .select(".datavis")
            .attr("height", height)
            .attr("width", width)

        const artsByMat = d3.rollup(data, v => v.length, d => d.material_type);
        const x = d3.scaleBand()
            .domain(Array.from(artsByMat.keys()))
            .range([margin.left, width - margin.right]);

        const y = d3.scaleLinear()
            .domain([0, Math.max(...Array.from(artsByMat.values()))])
            .range([height - margin.bottom, margin.top])

        svg.selectAll("rect")
            .attr("fill", "#000")
            .data(artsByMat)
            .enter().append("rect")
            .attr("fill", "#000")
            .attr("y", d => y(d[1]))
            .attr("x", d => x(d[0]))
            .attr("width", x.bandwidth() - 1)
            .attr("height", d => height - y(d[1]) - margin.bottom);

        const switchPoint = height - margin.bottom - 15
            console.log(switchPoint)

        svg.selectAll("text")
            .data(artsByMat)
            .enter().append("text")
            .text(d => d[1])
            .attr("text-anchor", "middle")
            .attr("fill", d => {if(y(d[1]) <= switchPoint) {return "#FFF"}else{return "#000"}})
            .attr("y", d => {if(y(d[1]) <= switchPoint) {return y(d[1]) + 15;}else{return y(d[1]) - 1;}})
            .attr("x", d => x(d[0]) + x.bandwidth() * 0.5);

        const xAxis = d3.axisBottom(x)
        svg.append("g")
            .attr("transform", "translate(0, " + (height - margin.bottom) + ")")
            .call(xAxis)
    })


