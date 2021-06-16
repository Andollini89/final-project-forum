

function editTopic(t_id){
    const topicaCardDiv = document.querySelector(`#topic-card-${t_id}`);
    const topicDivs = document.querySelectorAll(`#topic-card-${t_id} > div`);
    console.log(topicDivs[1])

    topicDivs.forEach(div => {
        div.style.display = 'none'
    })


    ClassicEditor
        .create( document.querySelector( `#body${t_id}` ), )
        .catch( error => {
            console.error( error );
        } );
    

    
    

}