let gpForm = document.getElementById('grandpy_form')
let submitBtn = document.getElementById('form_submit_btn')

gpForm.addEventListener('submit', (ev) => {
    let queryTxt = document.getElementById('form_input_txt').value
    fetch("/api?query=" + queryTxt)
        .then((resp) => resp.json())
        .then((data) => {
            const respElm = document.getElementById('bot_response')

            // create question span
            const qNode = document.createElement('span')
            qNode.classList.add('question')
            qNode.innerText = queryTxt

            // create response span
            let rNode = document.createElement('span')
            rNode.classList.add('answer')
            
            // create map div
            let mapNode = document.createElement('div')
            // use timestamp for unique ID
            const mapid = Date.now().toString()
            mapNode.id = mapid
            // fix height and width
            mapNode.classList.add('mapbox')
            
            // add map node to response node
            rNode.append(mapNode)
            // add response text to response node
            introText = data['wiki_extract'] != null ? data['wiki_extract'] : "Je n'ai rien trouvé à ce sujet :sad:"
            
            rNode.append(document.createElement('span').innerText = introText)

            // insert question
            respElm.insertBefore(qNode, respElm.firstChild)
            // insert answer
            respElm.insertBefore(rNode, respElm.firstChild)
            
            // manipulate map
            const mymap = L.map(mapid).setView([data['coords'][0], data['coords'][1]], 13)
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(mymap);

        })
    ev.preventDefault()
    return false
})