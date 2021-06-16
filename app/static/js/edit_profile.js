document.addEventListener('DOMContentLoaded', function(){
    const paragrafs = document.querySelectorAll('p')
    const labels = document.querySelectorAll('label')
    const inputs = document.querySelectorAll('p > input')

    paragrafs.forEach(p => {
        p.className = 'row';
    })
    labels.forEach(l => {
        l.className = 'col-2';
    })
    inputs.forEach(i => {
        i.className = 'col-7 ofset-2';
    })
})