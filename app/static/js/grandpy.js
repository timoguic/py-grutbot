let gpForm = document.getElementById('grandpy_form')
let submitBtn = document.getElementById('form_submit_btn')

gpForm.addEventListener('submit', (ev) => {
    let queryTxt = document.getElementById('form_input_txt').value
    fetch("/api?query=" + queryTxt)
        .then((resp) => resp.json())
        .then((data) => {
            console.log(data)
            const respElm = document.getElementById('bot_response')

            // create question node
            const qNodeRow = document.createElement('div')
            qNodeRow.classList.add('row')
            const qNode = document.createElement('div')
            qNode.classList.add('col', 's9', 'm6', 'question')
            qNode.innerHTML = '<p>' + queryTxt + '</p>'
            qNodeRow.append(qNode)

            // create response span
            const rNodeRow = document.createElement('div')
            rNodeRow.classList.add('row')

            const rNode = document.createElement('div')
            rNode.classList.add('col', 's11', 'offset-s1', 'm10', 'offset-m2', 'answer')
            rNode.style.padding = "1em"
            rNodeRow.append(rNode)

            let answerNodeWrapper = document.createElement('div')
            answerNodeWrapper.classList.add('row')
            rNode.append(answerNodeWrapper)

            // insert question
            respElm.insertBefore(qNodeRow, respElm.firstChild)
            // insert answer
            respElm.insertBefore(rNodeRow, respElm.firstChild)
            
            if (data['parsed'] != false) {

                if (data['coords'] != false) {
                    // create map div
                    let mapNode = document.createElement('div')
                    // use timestamp for unique ID
                    const mapid = Date.now().toString()
                    mapNode.id = mapid
                    // fix height and width
                    mapNode.classList.add('mapbox', 'col', 's12', 'm4')
                    
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
                answerText = document.createElement('div')
                answerText.innerHTML = introText
                answerText.classList.add('col', 's12', 'm8')
                answerNodeWrapper.append(answerText)
                
            } else {
                rNode.innerHTML = "<p>Désolé, je n'ai pas compris la question. C'en était une?</p>" + 
                "<pre><small>" + data['message'] + "</pre>"
            }
            
        })
    ev.preventDefault()
    return false
})