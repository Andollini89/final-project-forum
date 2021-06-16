document.addEventListener('DOMContentLoaded', function(){
    const plus_sign = document.getElementById('plus')
    plus_sign.addEventListener('click', showForm);

})




function showForm(){
    const formDiv = document.getElementById('answer-form-div')
    
    if (formDiv.style.display === 'block'){
        formDiv.style.display = 'none';
        window.scrollTo(0,0)
        console.log('fatto')
    }
    else{
        formDiv.style.display = 'block';
        let pos= formDiv.offsetTop
        console.log(pos);
        console.log('unfatto');
        window.scrollTo(0, pos);
    }
    
}
