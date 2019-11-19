function readProfile(listOfMetrics){
    text = readTextFile("../../Backend/userData.txt");
    textByLanes = text.split("\n")
    window.UserID = textByLanes[0].split(":")[1]
    window.UserName = textByLanes[1].split(":")[1]
    window.Doctor = textByLanes[2].split(":")[1]
    window.Hospital = textByLanes[3].split(":")[1]
    window.HospitalAddr = textByLanes[4].split(":")[1]
    window.ContactPhone = textByLanes[5].split(":")[1]
    window.Captors = textByLanes[6].split(":")[1]
    window.numCaptors = Captors.split(",").length
    var i = 0
    for (i = 0; i < numCaptors; i++) {
        firstSplit = textByLanes[7+i].split(";");
        secondSplit = firstSplit[1].split(",");
        var metricToAdd = {Name: firstSplit[0],downWarn: parseInt(secondSplit[0].split(":")[1]), topWarn: parseInt(secondSplit[1].split(":")[1]) , downlimit: parseInt(secondSplit[2].split(":")[1]), toplimit: parseInt(secondSplit[3].split(":")[1]), downpossible: parseInt(secondSplit[4].split(":")[1]) , toppossible: parseInt(secondSplit[5].split(":")[1]), unit: secondSplit[6].split(":")[1]}
        console.log(metricToAdd)
        listOfMetrics.push(metricToAdd)
    }
}
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
        }
        };
    data = this.getData(metricList.Name);
    var dataForm = {
      x: data.x,
      y: data.y,
      type: 'markers',
      marker: {
        size: 4,
        color: "#000000"
      }
    };
    var downlimit = {
        x: [getDateDownLimit(),getDateTopLimit()],
        y: [metricList.downlimit, metricList.downlimit],
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        fillcolor: "rgba(196, 19, 0, 0.5)"
    }
    var downWarn = {
        x: [getDateDownLimit(),getDateTopLimit()],
        y: [metricList.downWarn,metricList.downWarn],
        fill: 'tonexty',
        type: 'scatter',
        mode: 'none',
        fillcolor: "rgba(255, 255, 102,0.5)"
    }
    var neutral = {
        x: [getDateDownLimit(),getDateTopLimit()],
        y: [metricList.topWarn, metricList.topWarn],
        fill: 'tonexty',
        type: 'scatter',
        mode: 'none',
        fillcolor: 'rgba(0, 255, 34,0.2)'
    }
    var topWarn = {
        x: [getDateDownLimit(),getDateTopLimit()],
        y: [metricList.toplimit,metricList.toplimit],
        fill: 'tonexty',
        type: 'scatter',
        mode: 'none',
        fillcolor: "rgba(255, 255, 102,0.5)"
    }
    var toplimit = {
        x: [getDateDownLimit(),getDateTopLimit()],
        y: [metricList.toppossible,metricList.toppossible],
        fill: 'tonexty',
        type: 'scatter',
        mode: 'none',
        fillcolor: "rgba(196, 19, 0, 0.5)"
    }
    var totalData = [downlimit,downWarn,neutral,topWarn,toplimit,dataForm]
    Plotly.newPlot(metricList.Name,totalData,layout,{staticPlot: true});
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


var listOfMetrics = [];

//To be done the adaptative template
//var listOfMetrics;

readProfile(listOfMetrics)

createPlotlyDisplay(listOfMetrics);

for (let metric in listOfMetrics)
{
    overwriteCharts(listOfMetrics[metric]);
    setInterval(function(){overwriteCharts(listOfMetrics[metric]);},5000)
}



