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

gpForm.addEventListener('submit', (ev) => {
    let queryTxt = document.getElementById('form_input_txt').value
    fetch("/api?query=" + queryTxt)
        .then((resp) => resp.json())
        .then((data) => {
            console.log(data)
            const respElm = document.getElementById('bot_response')

            // create question node
            const qNodeRow = createRow()
            const qNode = createCol('s9', 'm6', 'question')
            qNode.innerHTML = '<p>' + queryTxt + '</p>'
            qNodeRow.append(qNode)

            // create response span
            const rNodeRow = createRow()

            const rNode = createCol('s11', 'offset-s1', 'm10', 'offset-m2', 'answer')
            rNode.style.padding = "1em"
            rNodeRow.append(rNode)

            let answerNodeWrapper = createRow()
            rNode.append(answerNodeWrapper)

            // insert question
            respElm.insertBefore(qNodeRow, respElm.firstChild)
            // insert answer
            respElm.insertBefore(rNodeRow, respElm.firstChild)
            
            if (data['parsed'] != false) {

                if (data['coords'] != false) {
                    // use timestamp for unique ID
                    const mapid = Date.now().toString()
                    // create map div
                    const mapNode = createCol('mapbox', 's12', 'm4')
                    mapNode.id = mapid
                    
                    // add map node to response node
                    answerNodeWrapper.append(mapNode)

                    // manipulate map
                    const mymap = L.map(mapid).setView([data['coords'][0], data['coords'][1]], 13)
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    }).addTo(mymap);
                }

                // add response text to response node
                introText = typeof data['wiki_extract'] !== 'undefined' ? data['wiki_extract'] : "<p>Désolé, je n'ai rien trouvé! :sad:</p>"
                answerText = createCol('s12', 'm8')
                answerText.innerHTML = introText
                answerNodeWrapper.append(answerText)
                
            } else {
                rNode.innerHTML = "<p>Désolé, je n'ai pas compris la question. C'en était une?</p>" + 
                "<pre><small>" + data['message'] + "</pre>"
            }
            
        })
    ev.preventDefault()
    return false
})