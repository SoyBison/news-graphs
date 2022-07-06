
margin = ({top: 10, right: 40, bottom: 60, left: 30})
height = 500 + margin.top + margin.bottom
width = 800 + margin.left + margin.right
let y, x, svg
const switchPoint = height - margin.bottom - 15

data = d3.csv(window.location.href + "/data")
    .then(data => {
        svg = d3
            .select(".datavis")
            .attr("height", height)
            .attr("width", width)

        const artsByMat = d3.rollup(data, v => v.length, d => d.material_type);
        x = d3.scaleBand()
            .domain(Array.from(artsByMat.keys()))
            .range([margin.left, width - margin.right]);

        y = d3.scaleLinear()
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

let intervalID = window.setInterval(reloadData, 60000)

function reloadData(){
        d3.csv(window.location.href + "/data")
            .then(data => {
                const artsByMat = d3.rollup(data, v => v.length, d => d.material_type);
                y.domain([0, Math.max(...Array.from(artsByMat.values()))])
                svg.selectAll('rect')
                    .filter(function(d, i) {return d[1] !== Array.from(artsByMat.values())[i]})
                    .attr('fill', '#F00')

                svg.selectAll("rect")
                    .data(artsByMat)
                    .transition()
                    .duration(60000)
                    .ease(d3.easeExpOut)
                    .attr("fill", "#000")
                    .attr("y", d => y(d[1]))
                    .attr("x", d => x(d[0]))
                    .attr("width", x.bandwidth() - 1)
                    .attr("height", d => height - y(d[1]) - margin.bottom);

                svg.selectAll("text")
                    .data(artsByMat)
                    .transition()
                    .duration(60000)
                    .ease(d3.easeExpOut)
                    .text(d => d[1])
                    .attr("text-anchor", "middle")
                    .attr("fill", d => {if(y(d[1]) <= switchPoint) {return "#FFF"}else{return "#000"}})
                    .attr("y", d => {if(y(d[1]) <= switchPoint) {return y(d[1]) + 15;}else{return y(d[1]) - 1;}})
                    .attr("x", d => x(d[0]) + x.bandwidth() * 0.5);
            })
}


