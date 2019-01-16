let gpForm = document.getElementById('grandpy_form')
let submitBtn = document.getElementById('form_submit_btn')

gpForm.addEventListener('submit', (ev) => {
    let queryTxt = document.getElementById('form_input_txt').value
    console.log(queryTxt)
    fetch("/api?query=" + queryTxt)
      .then((resp) => resp.json())
      .then((data) => {
          let respElm = document.getElementById('bot_response')

          let qNode = document.createElement('span')
          qNode.classList.add('question')
          let rNode1 = document.createElement('span')
          let rNode2 = document.createElement('span')
          rNode1.classList.add('answer')
          rNode2.classList.add('answer')
          
          qNode.innerText = queryTxt
          rNode1.innerText = data['wiki_extract']
          rNode2.innerText = data['coords'] + ' ' + data['wiki_url']
          
          respElm.insertBefore(qNode, respElm.firstChild)
          respElm.insertBefore(rNode2, respElm.firstChild)
          respElm.insertBefore(rNode1, respElm.firstChild)
      })
    ev.preventDefault()
    return false
})