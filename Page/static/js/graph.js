$(document).ready(function () {
    //选中要显示我们可视化图像的元素
    let svg = d3.select("#svg1"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    let simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) {
            return d.index;
        }))
        .force('collide', d3.forceCollide().radius(() => 10)) // collide 为节点指定一个radius区域来防止节点重叠。
        .force("charge", d3.forceManyBody().strength(-150))
        .force("center", d3.forceCenter(width / 2, height / 2-60));
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("GET","../../static/xml/data.xml",false);
    xmlhttp.send();
    xmlDoc=xmlhttp.responseXML;

    // 设置节点
    nodes = [];
    let data = xmlDoc.getElementsByTagName("course");
    for (let i = 0;i < data.length;i++){
        nodes.push({
            name:data[i].childNodes[1].innerHTML,
            description:data[i].childNodes[3].innerHTML
        })
    }

    let dragging = false;

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
        dragging = true;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
        dragging = false;
    }


    // 设置节点之间的连线
    edges = [];
    data = xmlDoc.getElementsByTagName("item");
    for (let i=0;i<data.length;i++){
        edges.push({
            source:parseInt(data[i].childNodes[1].childNodes[0].nodeValue),
            target:parseInt(data[i].childNodes[3].childNodes[0].nodeValue)})
    }
    let link = svg.append("g")
        .attr("class","links")
        .selectAll("line")
        .data(edges)
        .enter().append("line")
        .attr("stroke-width",'1');

    let node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes)
        .enter().append("circle")
        .attr("r", 20)
        .attr('name',function (d) {
            return d.name;
        })
        .attr('description',function (d) {
            return d.description
        })
        // .attr('class','inactive')
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    simulation
        .nodes(nodes)
        .on("tick", ticked);
    simulation.force("link")
        .links(edges);


    //设置节点上显示的文本
    let text = svg.append("g")
        .attr("class", "texts")
        .selectAll("text")
        .data(nodes)
        .enter().append("text")
        .attr("font-size", function(d) {
            return "13px";
        })
        .attr("fill", function(d) {
            // return color(d.group);
            return "rgba(255,255,255)";
        })
        .attr('class','inactive')
        .text(function(d) {
            return d.name;
        })
        .attr('text-anchor', 'middle')
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));


    function ticked() {
        link
            .attr("x1", function(d) {
                return d.source.x;
            })
            .attr("y1", function(d) {
                return d.source.y;
            })
            .attr("x2", function(d) {
                return d.target.x;
            })
            .attr("y2", function(d) {
                return d.target.y;
            });
        node.attr("cx", function(d) {
            return d.x;
        })
            .attr("cy", function(d) {
                return d.y;
            });

        text.
        attr('transform', function(d) {
            return 'translate(' + d.x + ',' + (d.y) + ')';
        });
    }

    // 处理搜索框，实现搜索功能
    $('#search1 input').keyup(function(event) {
        if ($(this).val() == '') {
            d3.select('#svg1 .texts').selectAll('text').attr('class', '');
            d3.select('#svg1 .nodes').selectAll('circle').attr('class', '');
            d3.select('#svg1 .links').selectAll('line').attr('class', '');
        } else {
            var name = $(this).val();
            d3.select('#svg1 .nodes').selectAll('circle').attr('class', function (d) {
                //找到包含包含输入的变量,显示,否则不显示
                if (d.name.indexOf(name) >= 0) {
                    return '';
                } else {
                    /*d.name代表当前节点的内容*/
                    if (d.name == name) {
                        return '';
                    }

                    for (let i = 0; i < edges.length; i++) {
                        if (edges[i]['source'].name.indexOf(d.name)>=0 && edges[i]['target'].name.indexOf(name)>=0) {
                            return '';
                        }
                        if (edges[i]['target'].name.indexOf(d.name)>=0 && edges[i]['source'].name.indexOf(name)>=0) {
                            return '';
                        }
                    }
                    return 'inactive';
                }

            });
            d3.select('#svg1 .texts').selectAll('text').attr('class', function (d) {

                if (d.name.indexOf(name) >= 0) {
                    return '';
                } else {
                    for (let i = 0; i < edges.length; i++) {
                        if (edges[i]['source'].name.indexOf(d.name) >= 0 && edges[i]['target'].name.indexOf(name) >= 0) {
                            return '';
                        }
                        if (edges[i]['target'].name.indexOf(d.name) >= 0 && edges[i]['source'].name.indexOf(name) >= 0) {
                            return '';
                        }
                    }
                }
                return 'inactive';
            });
            d3.select("#svg1 .links").selectAll('line').attr('class', function (d) {
                for (let i = 0; i < edges.length; i++) {
                    if (d['source'].name.indexOf(name)>=0||d['target'].name.indexOf(name)>=0) {
                        return '';
                    }
                }
                return 'inactive';
            });
        }
    });

    // 处理鼠标悬浮的情况
    $('#svg1').on('mouseenter','.nodes circle',function (event) {
        if (!dragging) {
            // 获取当前课程的名字
            let name = $(this)[0].attributes.name.nodeValue;
            $('#info h4').text("课程名称: " + name);


            $('#info p').remove();

            $('#info').append("<p>课程描述:<span>"+$(this)[0].attributes[2].nodeValue+'</span></p>');

            d3.select('#svg1 .nodes').selectAll('circle')
                .attr("class", function (d) {
                    if (d.name == name) {
                        return "";
                    }
                    for (let i = 0; i < edges.length; i++) {
                        if (edges[i]['source'].name == name && edges[i]['target'].name == d.name) {
                            return '';
                        }
                        if (edges[i]['target'].name == name && edges[i]['source'].name == d.name) {
                            return '';
                        }
                    }
                    return "inactive";
                });

            d3.select('#svg1 .texts').selectAll('text')
                .attr("class", function (d) {
                    if (d.name==name) {
                        return '';
                    } else {
                        for (let i = 0; i < edges.length; i++) {
                            if (edges[i]['source'].name==d.name  && edges[i]['target'].name==name) {
                                return '';
                            }
                            if (edges[i]['target'].name==d.name&& edges[i]['source'].name==name ) {
                                return '';
                            }
                        }
                    }
                    return 'inactive';
                });

            d3.select("#svg1 .links").selectAll('line').attr('class', function (d) {
                for (let i = 0; i < edges.length; i++) {
                    if (d['source'].name==name||d['target'].name==name) {
                        return '';
                    }
                }
                return 'inactive';
            });
        }
    });
});
