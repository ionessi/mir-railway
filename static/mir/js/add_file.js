'use strict';

let tagsAdd = '';

document.addEventListener('DOMContentLoaded', () => {

});

function send(event) {

    let text = document.getElementById('text');
    let info = document.getElementById('info');

    if (file.files[0] == undefined && text.value == '') {
        event.preventDefault();
        info.innerText = 'нет текста сообщения или файла!';

    } else {
        document.getElementsByTagName('button')[0].disabled = 'true';
        document.getElementsByTagName('button')[1].disabled = 'true';
        info.innerText = 'сообщение отправляется!';
        document.getElementsByTagName('form')[0].submit();
    }
}

function sendComment(event) {
    let text = document.getElementById('text');
    let info = document.getElementById('info');

    if (file.files[0] == undefined && text.value == '') {
        event.preventDefault();
        info.innerText = 'нет текста комментария или файла!';

    } else {
        document.getElementsByTagName('button')[0].disabled = 'true';
        document.getElementsByTagName('button')[1].disabled = 'true';
        info.innerText = 'комментарий отправляется!';
        document.getElementsByTagName('form')[0].submit();
    }
}

function addFile(event, id) {
    event.preventDefault();
    event.stopImmediatePropagation();

    let f = document.getElementById(id);
    f.click();
    f.onchange = function(event) {
        document.getElementById('file_size').value = file.files[0].size;
        document.getElementById('info').innerText = file.files[0].name
    }
}

function getQuote(id, login, date) {
    let quote = document.getElementById(id).innerHTML;
    document.getElementById('quote_info').innerText = 'цитата добавлена';
    document.getElementById('quote').value = '<span class="w3-text-gray">' + quote + '<br/><span style="font-size: 11px;">' + login + ' &nbsp ' + date + '</span></span><br/><br/>';
    let el = document.getElementById('add_comment');
    el.scrollIntoView({behavior: "smooth"});
}

function addTag(tag) {
    document.getElementById('tags').value = document.getElementById('tags').value + tag + ' ';
}
