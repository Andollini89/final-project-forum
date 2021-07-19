document.addEventListener('DOMContentLoaded', function(){
    window.addEventListener("resize", swapDivs);
    swapDivs()
    checkCookies()
})
    
var icones = ['right','down', 'left'];

function redirectToForm(){
    window.location.href = '/new-topic'
}

function swapDivs(){
    const block_3 = document.getElementById('block-3')
    const arrow_3 = document.getElementById('arrow-3')
    const secondDiv = document.getElementById('second-div')
    const arrows = document.querySelectorAll('.suca')
    const span = document.getElementById('span')
    
    if (screen.width < 1000){
        
        secondDiv.prepend(block_3, arrow_3)
        arrows.forEach( e=>{
            e.innerHTML = '<i class="arrows fas fa-arrow-down"></i>'
        })
        arrows[1].classList.replace('w-50','w-100')
    } 
    else{
        secondDiv.append(arrow_3,block_3)
        for(let i = 0; i < arrows.length; i++){
            arrows[i].innerHTML= `<i class="arrows fas fa-arrow-${icones[i]}"></i>`
        }
        arrows[1].classList.replace('w-100','w-50')
        
    }
}

function addCookiesAgreement(){
    const cookiesBannerDiv = document.getElementById('cookies-banner')
    document.cookie = `GPDR=agreement; max-age=${30*86400}; path=/;`;
    cookiesBannerDiv.style.display='none'
}
function closeBanner(){
    document.getElementById('cookies-banner').style.display='none'
}
function checkCookies(){
    const cookie = getCookie('GPDR')
    if (cookie != null){
        document.getElementById('cookies-banner').style.display = 'none';
    }
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
