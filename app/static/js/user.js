

function editTopic(t_id){
    const topicaCardDiv = document.querySelector(`#topic-card-${t_id}`);
    const topicDivs = document.querySelectorAll(`#topic-card-${t_id} > div`);
    const editorForm = document.querySelector('#editor')
    const editorIFrame = document.querySelector('iframe')
    
    console.log(topicDivs[1].innerHTML)
    console.log(editorIFrame)

    editorForm.action = `/edittopic/${t_id}`
    editorForm.style.display = 'block'
    editorIFrame.contentDocument.querySelector('body').innerHTML = topicDivs[1].innerHTML
   

}

function deleteConfirmation(t_id){
    var result = confirm("Want to delete?");
    if (result) {
    deleteTopic(t_id)
}
}


function deleteTopic(t_id) {

    const topicDiv =  document.querySelector(`#topic-card-${t_id}`);
    const token = getCookie('csrftoken')

    fetch(`/edittopic/${t_id}`,{
        headers :{"X-CSRFToken":token},
        method:"DELETE",
        mode: "same-origin",
        body: JSON.stringify({
            id:t_id,
        })
    }).then(response=> response.json())
    .then(result => {
        console.log(result)
    })

    topicDiv.remove()
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