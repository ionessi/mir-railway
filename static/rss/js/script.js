'use strict';

document.addEventListener('DOMContentLoaded', () => {
    //console.log('izvestiya');
});

function openForm(id) {

    if (event.target.tagName !== 'A') {
        document.getElementById(id).className = 'w3-block';
    }
    
}

function send(event, id) {

    let tags = document.getElementById('tags_' + id);
    let text = document.getElementById('text_' + id);
    let info = document.getElementById('info_' + id);

    if (tags.value == '') {
        event.preventDefault();
        info.innerText = 'Введите хоть один тэг!';

    } else if (text.value == '') {
        event.preventDefault();
        info.innerText = 'нет текста сообщения!';
        
    } else {
        document.getElementById('but_' + id).disabled = 'true';
        //document.getElementsByTagName('button')[1].disabled = 'true';
        info.innerText = 'сообщение отправляется!';
        document.getElementById(id).submit();
    }
}
