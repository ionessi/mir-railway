'use strict';

document.addEventListener('DOMContentLoaded', () => {

});

function send(event) {
    event.preventDefault();
    
    let text = document.getElementById('text');
    let info = document.getElementById('info');
    let select = document.getElementsByTagName('select')[0];
    
    if (select.validity.valid) {
        if (file.files[0] == undefined && text.value == '') {
            info.innerText = 'нет текста сообщения или файла!';
            
        } else {
            document.getElementsByTagName('button')[0].disabled = 'true';
            document.getElementsByTagName('button')[1].disabled = 'true';
            info.innerText = 'сообщение отправляется!';
            document.getElementsByTagName('form')[0].submit();
        }
        
    } else {
        info.innerText = 'не выбран пользователь!';
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

