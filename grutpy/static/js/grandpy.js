let gpForm = document.getElementById('grandpy_form')
let submitBtn = document.getElementById('form_submit_btn')

function updateMap(coords, mapId) {
    let lat = coords[0]
    let lon = coords[1]
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
            console.log(data)
            const respElm = document.getElementById('bot_response')
            const templateElms = document.querySelectorAll('#chat_template > .row')
            let answerNode = templateElms[0].cloneNode(true)
            let questionNode = templateElms[1].cloneNode(true)
            console.log(templateElms)
            questionNode.querySelector('p').innerText = txtValue

            respElm.insertBefore(questionNode, respElm.firstChild)
            respElm.insertBefore(answerNode, respElm.firstChild)

            if (data['parsed'] != false) {
    
                if (data['coords'] != false) {                    
                    // use timestamp for unique ID
                    const mapid = Date.now().toString()

                    mapbox = answerNode.querySelector('.mapbox')
                    mapbox.id = mapid
                    updateMap(data['coords'], mapid)

                    answerNode.querySelector('.wiki').innerHTML = data['wiki']['extract']

                    answerNode.querySelector('.weather-icon').src = data['weather']['icon']
                    answerNode.querySelector('h6').append(
                        document.createTextNode(
                            data['weather']['temp'] + '°C, ' + data['weather']['description']
                        )
                    )

                    answerNode.querySelector('.webcam-location').innerText = data['webcam']['location']
                    answerNode.querySelector('.webcam-img').src = data['webcam']['img']

                }
            } else {
                answerNode.innerHTML = "<p>Désolé, je n'ai pas compris la question. C'en était une?</p>" + 
                "<pre><small>" + data['parsed'] + "</pre>"
            }
        })
}

gpForm.addEventListener('submit', (ev) => {
    let queryTxt = document.getElementById('form_input_txt').value
    submitData(queryTxt)    
    ev.preventDefault()
    return false
})