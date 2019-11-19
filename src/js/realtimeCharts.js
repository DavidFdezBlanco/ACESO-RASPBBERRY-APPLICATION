function getData(label) {
    text = readTextFile("../../Backend/data.txt");
    textByLanes = text.split("\n")
    var x = [];
    var y = []
    var labelSplitted,data;
    for (let line in textByLanes)
    {
        if(textByLanes[line] != ""){
            lineSplitted = textByLanes[line].split("]")
            if(lineSplitted[0].includes(label)){
                details = lineSplitted[1].split(",")
                y.push(details[0])
                x.push(details[2])
            }
        }
    }
    return {x,y};
}

function readTextFile(file)
{
    var text;
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                text = allText;
            }
        }
    }
    rawFile.send(null);
    return text
}

function getDateDownLimit(){
    var today = new Date();
    var month = parseInt(('0'+today.getMonth()).slice(-2)) + 1;
    var day = ('0'+today.getDate()).slice(-2);
    var hour = parseInt(('0'+today.getHours()).slice(-2)) - 2;
    var mins = ('0'+today.getMinutes()).slice(-2);
    var secs = ('0'+today.getSeconds()).slice(-2);
    var date = today.getFullYear()+'-'+month+'-'+day;
    var time = hour + ":" + mins + ":" + secs;
    return date + " " + time
}

function getDateTopLimit(){
    var today = new Date();
    var month = parseInt(('0'+today.getMonth()).slice(-2)) + 1;
    var day = ('0'+today.getDate()).slice(-2);
    var hour = parseInt(('0'+today.getHours()).slice(-2))-1;
    var mins = ('0'+today.getMinutes()).slice(-2);
    var secs = ('0'+today.getSeconds()).slice(-2);
    var date = today.getFullYear()+'-'+month+'-'+day;
    var time = hour + ":" + mins + ":" + secs;
    return date + " " + time
}

function overwriteCharts( metricList ){
    var down = getDateDownLimit()
    var top = getDateTopLimit()
    var layout =
        {
        title: metricList.Name,
        showlegend: false,
        xaxis: {
          type: 'date',
          range: [down, top],
          title: {
            text: 'Time',
            font: {
              size: 12,
              color: '#7f7f7f'
            }
          }
        },
        yaxis: {
          type: 'linear',
          range: [metricList.downpossible, metricList.toppossible],
          title: {
            text: metricList.unit,
            font:
              {
                  size: 12,
                  color: '#7f7f7f'
              }
           }
        },
        shapes:
            [
                {
                    type: 'line',
                    x0: getDateDownLimit(),
                    y0: metricList.downlimit,
                    x1: getDateTopLimit(),
                    y1:metricList.downlimit,
                    line:
                    {
                        color: 'rgb(255, 0, 0)',
                        width: 4
                    }
                },
                {
                    type: 'line',
                    x0: getDateDownLimit(),
                    y0: metricList.toplimit,
                    x1: getDateTopLimit(),
                    y1:metricList.toplimit,
                    line:
                    {
                        color: 'rgb(255, 0, 0)',
                        width: 4
                    }
                }
            ]
        };
    data = this.getData(metricList.Name);
    var dataForm = [{
      x: data.x,
      y: data.y,
      type: 'scatter',
      color: "#fffff"
    }];
    console.log(metricList.Name)
    Plotly.newPlot(metricList.Name,dataForm,layout,{staticPlot: true});
}

function createmyElement(metricList){
   return [
           '<div class="swiper-slide hero-content-wrap">',
            '<div class="hero-content-overlay position-absolute w-100 h-100">',
             '<div class="container h-100">',
              '<div class="row h-100">',
               '<div class="col-12 col-lg-6 d-flex flex-column justify-content-center align-items-start">',
                 '<div id="', metricName, '"></div>',
                '</div><!-- .col -->',
               '</div><!-- .row -->',
              '</div><!-- .container -->',
             '</div><!-- .hero-content-overlay -->',
            '</div><!-- .hero-content-wrap -->'
          ].join('\n');
}

function createPlotlyDisplay(listOfMetrics)
{
    //Retrieve body element
    var body = document.getElementsByTagName('body')[0];
    
    //creating swipper and wrapper divs
    swipCont = document.createElement("div");
    swipCont.className = "swiper-container hero-slider";

    swipWrap = document.createElement("div");
    swipWrap.className = "swiper-wrapper";
    swipWrap.id = "swipper";
    
    for (let metric in listOfMetrics)
    {
        createGraph(listOfMetrics[metric],swipWrap,swipCont);
    }
    
    pagWrap = document.createElement("div");
    pagWrap.className = "pagination-wrap position-absolute w-100";
    swipPag = document.createElement("div");
    swipPag.className = "swiper-pagination d-flex flex-row flex-md-column";

    body.appendChild(swipCont);
    pagWrap.appendChild(swipPag);
    swipCont.appendChild(pagWrap);

    body.insertBefore(swipCont,body.childNodes[2])
    
}

function createGraph(metric, swipWrap, swipCont)
{
    swipSlide = document.createElement("div");
    swipSlide.className = "swiper-slide hero-content-wrap";

    heroCont = document.createElement("div");
    heroCont.className = "hero-content-overlay position-absolute w-100 h-100";

    contain = document.createElement("div");
    contain.className = "container h-100";

    row = document.createElement("div");
    row.className = "row h-100";

    col = document.createElement("div");
    col.className = "col-12 col-lg-6 d-flex flex-column justify-content-center align-items-start";
    
    flag = document.createElement("div");
    flag.id = metric.Name;
    
    col.appendChild(flag);
    row.appendChild(col);
    contain.appendChild(row);
    heroCont.appendChild(contain);
    swipSlide.appendChild(heroCont);
    swipWrap.appendChild(swipSlide);
    swipCont.appendChild(swipWrap);
}


var listOfMetrics = [
                     {Name: "pulse",downlimit: 60,toplimit: 140, downpossible:40, toppossible: 170, unit: "BPM" },
                     {Name: "temperature",downlimit: 35,toplimit: 38, downpossible:34, toppossible: 40, unit: "ºC"}
                    ];

//To be done the adaptative template


createPlotlyDisplay(listOfMetrics);

for (let metric in listOfMetrics)
{
    overwriteCharts(listOfMetrics[metric]);
    setInterval(function(){overwriteCharts(listOfMetrics[metric]);},5000)
}



