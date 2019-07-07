let gpForm = document.getElementById('grandpy_form')
let submitBtn = document.getElementById('form_submit_btn')

function createRow(...extraClasses) {
    const elm = document.createElement('div')
    elm.classList.add('row')
    extraClasses.forEach(cls => elm.classList.add(cls))
    return elm
}

function createCol(...extraClasses) {
    const elm = document.createElement('div')
    elm.classList.add('col')
    extraClasses.forEach(cls => elm.classList.add(cls))
    return elm
}

function createWeatherNode(icon, temperature, description) {
    // create image and text nodes
    const weatherText = document.createElement('h6')
    weatherText.classList.add('weather-description')
    // weatherText.append(document.createTextNode('Météo: '))
    
    
    const weatherImg = document.createElement('img')
    weatherImg.src = icon
    weatherImg.classList.add('weather-icon')

    weatherText.append(weatherImg)
    weatherText.append(document.createTextNode(temperature + '°C, ' + description))
    
    return weatherText
}

function createQuestionNode(txtVal) {
    // create question node
    const qNodeRow = createRow()
    const qNode = createCol('s9', 'm6', 'question')
    qNode.innerHTML = '<p>' + txtVal + '</p>'
    qNodeRow.append(qNode)

    return qNodeRow
}

function createMapDiv(mapId) {
    // create map div
    const mapNode = document.createElement('div')
    mapNode.classList.add('mapbox')
    mapNode.id = mapId

    return mapNode
}

function updateMap(lat, lon, mapId) {
    // manipulate map
    const mymap = L.map(mapId).setView([lat, lon], 13)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mymap)
}

function submitData(txtValue) {
    fetch("/api?query=" + txtValue)
        .then((resp) => resp.json())
        .then((data) => {
            const respElm = document.getElementById('bot_response')
            
            // insert question
            questionNode = createQuestionNode(txtValue)
            respElm.insertBefore(questionNode, respElm.firstChild)

            // create response row
            const rNodeRow = createRow()
    
            const rNode = createCol('s11', 'offset-s1', 'm10', 'offset-m2', 'answer')
            rNode.style.padding = "1em"
            rNodeRow.append(rNode)
    
            let answerNodeWrapper = createRow()
            rNode.append(answerNodeWrapper)
    
            // insert answer
            respElm.insertBefore(rNodeRow, respElm.firstChild)
            
            if (data['parsed'] != false) {
    
                if (data['coords'] != false) {
                    // create wrapper
                    mapNodeWrapper = createCol('s12', 'm4')
                    answerNodeWrapper.append(mapNodeWrapper)
                    
                    // use timestamp for unique ID
                    const mapid = Date.now().toString()
                    
                    mapDiv = createMapDiv(mapid)
                    mapNodeWrapper.append(mapDiv)
                    updateMap(data['coords'][0], data['coords'][1], mapid)

                    weatherDiv = createWeatherNode(
                        data['weather_icon'],
                        data['weather_temp'],
                        data['weather_description']
                    )
                    mapNodeWrapper.append(weatherDiv)

                }
    
                // add response text to response node
                introText = typeof data['wiki_extract'] !== 'undefined' ? data['wiki_extract'] : "<p>Désolé, je n'ai rien trouvé! :sad:</p>"
                answerText = createCol('s12', 'm8')
                wikiDiv = document.createElement('div')
                wikiDiv.innerHTML = introText
                answerText.append(wikiDiv)

                webcamDiv = document.createElement('div')
                webcamDiv.classList.add('webcam')
                webcamH6 = document.createElement('h6')
                webcamH6.textContent = 'Webcam'
                webcamDiv.append(webcamH6)
                webcamImg = document.createElement('img')
                webcamImg.src = data['webcam_img']
                webcamDiv.append(webcamImg)
                webcamP = document.createElement('p')
                webcamP.innerText = data['webcam_location']
                webcamP.classList.add('webcam-location')
                webcamDiv.append(webcamP)

                answerText.append(webcamDiv)

                answerNodeWrapper.append(answerText)
                
            } else {
                rNode.innerHTML = "<p>Désolé, je n'ai pas compris la question. C'en était une?</p>" + 
                "<pre><small>" + data['message'] + "</pre>"
            }
            
        })
}

gpForm.addEventListener('submit', (ev) => {
    let queryTxt = document.getElementById('form_input_txt').value
    submitData(queryTxt)    
    ev.preventDefault()
    return false
})

function init() {
    submitData('los angeles?')
}

window.addEventListener('DOMContentLoaded', init, false)
