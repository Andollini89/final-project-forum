
function editTopic(t_id){
    const topicDiv = document.querySelector('#topic-body')
    const editorForm = document.querySelector('#editor')
    const editorIFrame = document.querySelector('iframe')
    
   

    editorForm.action = `/edittopic/${t_id}`
    editorForm.style.display = 'block'
    editorIFrame.contentDocument.querySelector('body').innerHTML = topicDiv.innerHTML
   

}
function editAnswer(a_id){

    const answerDiv = document.querySelector(`#answer-body-${a_id}`)
    const editorForm = document.querySelector('#answer')
    const editorIFrame = document.querySelectorAll('iframe')
    
   

    editorForm.action = `/editanswer/${a_id}`
    editorForm.style.display = 'block'
    editorIFrame[1].contentDocument.querySelector('body').innerHTML = answerDiv.innerHTML
    console.log(editorIFrame[1].innerHTML)

}
function deleteConfirmation(page,id){
    var result = confirm("Want to delete?");
    console.log(result)
    if (result === true) {
        deleteTopic(page, id)
    }
    else{
        return
    }
    if (page === 'answer'){
        document.getElementById(`answer-card-${id}`).remove()
    }
    else{
        window.location.replace('/')
    }
    
}


function deleteTopic(page,id) {

    const token = getCookie('csrftoken')

    fetch(`/edit${page}/${id}`,{
        headers :{"X-CSRFToken":token},
        method:"DELETE",
        mode: "same-origin",
        body: JSON.stringify({
            id:id,
        })
    }).then(response=> response.json())
    .then(result => {
        console.log(result)
    })

}

function closeTopic(id){
    var result = confirm('do you want to close answers to this topic?')
    const token = getCookie('csrftoken')
    if (result === true){
        fetch(`/edittopic/${id}`,{
            headers :{"X-CSRFToken":token},
            method:"PUT",
            mode: "same-origin",
            body: JSON.stringify({
                id : id,
                closed:true,
            })
        }).then(response=> response.json())
        .then(result => {
            console.log(result)
        })
        document.getElementById('commands').remove()
    }
    else{
        return
    }

}

function correctAnswer(a_id, status){
    const token = getCookie('csrftoken')


    if (status){
        var result = confirm('Do you want to unmark this answer as correct?')
    }
    else{
        var result = confirm('Do you want to mark this answer as the correct one?')
    }
    

    if (result == true){
        fetch(`/editanswer/${a_id}`,{
            headers :{"X-CSRFToken":token},
            method:"PUT",
            mode: "same-origin",
            body: JSON.stringify({
                id : a_id,
                correct: !status,
            })
        }).then(response=> response.json())
        .then(result => {
            console.log(result)
        })

        location.reload()
    }
    else{
        return
    }
    

}

function upVote(a_id){

    const token = getCookie('csrftoken')

    fetch("/add-vote",{
        headers :{"X-CSRFToken":token},
            method:"POST",
            mode: "same-origin",
            body: JSON.stringify({
                id : a_id,
                vote: 1,
            })
        }).then(response=> response.json())
        .then(result => {
            console.log(result)
            document.getElementById('votes_count').innerHTML=result['updatevotes']
        })
   
}
function downVote(a_id){

    const token = getCookie('csrftoken')

    fetch("/add-vote",{
        headers :{"X-CSRFToken":token},
            method:"POST",
            mode: "same-origin",
            body: JSON.stringify({
                id : a_id,
                vote: -1,
            })
        }).then(response=> response.json())
        .then(result => {
            console.log(result)
            document.getElementById('votes_count').innerHTML=result['updatevotes']
        })
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
