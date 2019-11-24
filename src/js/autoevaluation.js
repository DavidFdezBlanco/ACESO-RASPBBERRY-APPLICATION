const fs = require('fs')

function readProfile(listOfMetrics)
{
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
        var metricToAdd = {Name: firstSplit[0],downWarn: parseInt(secondSplit[0].split(":")[1]), topWarn: parseInt(secondSplit[1].split(":")[1]) , downlimit: parseInt(secondSplit[2].split(":")[1]), toplimit: parseInt(secondSplit[3].split(":")[1]), downpossible: parseInt(secondSplit[4].split(":")[1]) , toppossible: parseInt(secondSplit[5].split(":")[1]), unit: secondSplit[6].split(":")[1],
            short: secondSplit[7].split(":")[1]
        }
        listOfMetrics.push(metricToAdd)
    }
}

function readAutoevalText(file){
    text = readTextFile("../../Backend/receivedFiles/autoeval/autoevaluationData.txt");
    textByLanes = text.split("\n")
    window.listOfQuestions = []
    window.title = textByLanes[0].split(":")[1]
    for(line in textByLanes){
        listOfQuestions.push(textByLanes[line])
    }
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

function createRepport(metric, swipWrap, swipCont)
{
    //Retrieve body element
    var body = document.getElementsByTagName('body')[0];
    
    //Container contact
    containerContact100=document.createElement("div");
    containerContact100.className = 'container-contact100';
    containerContact100.style.cssText='margin-top: 110px';
    
    //button
    buttonCon100 =document.createElement("button");
    buttonCon100.className='contact100-btn-show';
    buttonCon100.setAttribute("onclick", "displayForm()");
    
    //iCon100
    iCon100 = document.createElement("i");
    iCon100.className="fa fa-check-square-o";
    iCon100.setAttribute('aria-hidden',"true");
    
    //Appending
    buttonCon100.appendChild(iCon100);
    containerContact100.appendChild(buttonCon100);
    
    
    //Wrap contact100
    wrapContact100 = document.createElement("div");
    wrapContact100.className = "wrap-contact100";
//    wrapContact100.style.cssText = "display: block;"
    
    //button hide
    buttonHide = document.createElement("button");
    buttonHide.className = "contact100-btn-hide";
    buttonHide.setAttribute("onclick", "closeForm()");
    
    //iClose
    iClose = document.createElement("i");
    iClose.className = "fa fa-close";
    iClose.setAttribute('aria-hidden',"true");
    
    //appending button hide
    buttonHide.appendChild(iClose);
    wrapContact100.appendChild(buttonHide);
    
    //Form
    //To be modified with the txt
    contactFormCont =document.createElement("form");
    contactFormCont.className='contact100-form validate-form';
    
    //Title
    contactFormTit =document.createElement("span");
    contactFormTit.className='contact100-form-title';
    contactFormTit.id='titleSpan';
    contactFormTit.innerHTML = title
    
    //Submit button
    submitButtonCont  = document.createElement("div");
    submitButtonCont.className = "container-contact100-form-btn";
    
    button = document.createElement("button");
    button.className = "contact100-form-btn";
    button.setAttribute("onclick", "submitFunction()");
    
    spanText = document.createElement("span");
    
    iSubmit = document.createElement("i")
    iSubmit.className = "fa fa-long-arrow-right m-l-7"
    iSubmit.setAttribute('aria-hidden',"true");
    
    //Append button submit
    
    spanText.appendChild(iSubmit)
    button.appendChild(spanText)
    submitButtonCont.appendChild(button)
    
    startAnswer(title, listOfQuestions)
    
    //Final append
    contactFormCont.appendChild(contactFormTit)
    for (index in listOfQuestions)
    {
        lineSplitted = listOfQuestions[index].split(":")
        if(lineSplitted[0]=="Multi"){
            contactFormCont.append(createMultichoice(index,lineSplitted[1]))
        }
        if(lineSplitted[0]=="TextArea"){
            contactFormCont.append(createTextarea(index,lineSplitted[1]))
        }
    }
    contactFormCont.appendChild(submitButtonCont)
    wrapContact100.appendChild(contactFormCont)
    containerContact100.appendChild(wrapContact100)
    body.appendChild(containerContact100);
    body.insertBefore(containerContact100,body.childNodes[5])
    
    
}
function startAnswer(title, listOfQuestions)
{
    window.data = []
    data.push("Title:"+title)
    for (index in listOfQuestions)
    {
        if(index!=0){
            data.push(listOfQuestions[index]+";Answer:")
        }
    }
    //function to start the file data before the clicking into the submit button
}
function createMultichoice(numberOfMultichoices, question)
{
    
    wrapInput = document.createElement("div")
    wrapInput.className = "wrap-input100"
    wrapInput.style.cssText = "padding-bottom: 140px"
    
    showcase = document.createElement("div")
    showcase.className = "showcase"
    
    ratingSystem3 = document.createElement("div")
    ratingSystem3.className = "rating-system3"
    
    titleh3 = document.createElement("h3")
    titleh3.style.cssText = "padding-bottom: 20px"
    titleh3.innerHTML = question
    
    ratingSystem3.append(titleh3)
    //5 stars
    for (i = 0; i < 5; i++)
    {
        radio = document.createElement("input")
        radio.setAttribute("type","radio")
        radio.setAttribute("name","rate3"+String(numberOfMultichoices))
        radio.setAttribute("id","star"+String(i)+"_3_"+String(numberOfMultichoices))
        
        label = document.createElement("label")
        label.setAttribute("for","star"+String(i)+"_3_"+String(numberOfMultichoices))
        label.id ="star"+String(i)+"_3_"+String(numberOfMultichoices)
        label.setAttribute("onclick", "chooseStar('"+i+"','"+String(numberOfMultichoices)+"')");
        ratingSystem3.append(radio)
        ratingSystem3.append(label)
    }
    text = document.createElement("div")
    text.className = "text"
    ratingSystem3.append(text)
    showcase.append(ratingSystem3)
    wrapInput.append(showcase)
    return wrapInput
}
function chooseStar(index, numChoic)
{
    var answerMultichoice
    switch(String(index)) {
      case '0':
        answerMultichoice = "5/5"
        break;
      case '1':
        answerMultichoice = "4/5"
        break;
      case '2':
        answerMultichoice = "3/5"
        break;
      case '3':
        answerMultichoice = "2/5"
        break;
      case '4':
        answerMultichoice = "1/5"
        break;
      default:
        answerMultichoice = "Not completed"
        break;
    }
    newline = data[numChoic].split(";")
    data[numChoic] = newline[0] + ";Answer:" + answerMultichoice
}

function createTextarea(numberTextArea, Question){
    
    valinput = document.createElement("div")
    valinput.className = "wrap-input100 validate-input"
    valinput.setAttribute("data-validate","Message is required")
    
    labelInput = document.createElement("span")
    labelInput.innerHTML = Question
    labelInput.className = "label-input100"
    
    textArea = document.createElement("textarea")
    textArea.className = "input100"
    textArea.id ="message"+String(numberTextArea)
    textArea.setAttribute("name","message"+String(numberTextArea))
    textArea.setAttribute("placeholder", "Please answer here...")
    
    focusInput = document.createElement("span")
    focusInput.className = "focus-input100"
    
    valinput.append(labelInput)
    valinput.append(textArea)
    valinput.append(focusInput)
    return valinput
}
function getTextAreasContent()
{
    for (index in listOfQuestions)
    {
        lineSplitted = listOfQuestions[index].split(":")
        if(lineSplitted[0]=="TextArea"){
            newline = data[index].split(";")
            data[index] = newline[0] + ";Answer:" + document.getElementById("message"+String(index)).value
        }
    }
}
function displayForm()
{
    var wrapContact100 = document.getElementsByClassName("wrap-contact100")[0];
    wrapContact100.style.cssText = "display: block;"
}
function closeForm()
{
    var wrapContact100 = document.getElementsByClassName("wrap-contact100")[0];
    wrapContact100.style.cssText = "display: none;"
}
function submitFunction()
{
    getTextAreasContent()
    var dataOutput
    for (line in data)
    {
       dataOutput += data[line] + "\n"
    }
    var start = Date.now();
    fs.writeFile("Backend/filesToSend/Autoeval/"+String(start)+".txt", dataOutput, (err) => {
        if(err){
            alert("An error ocurred creating the file "+ err.message)
        }
        else
        {
            alert("The file has been succesfully saved");
        }
    });
    fs.unlinkSync("Backend/receivedFiles/autoeval/autoevaluationData.txt");
}
function fullfillReport()
{
    document.getElementById('buttonPhone').innerHTML = ContactPhone;
}

var listOfMetrics = [];
readProfile(listOfMetrics);

readAutoevalText()
createRepport();
fullfillReport();

