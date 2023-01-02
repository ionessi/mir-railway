
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('text').value = '';
    document.getElementById('file').value = '';
    document.getElementById('file_size').value = '';
    
    document.getElementById('text').disabled = true;
    document.getElementById('share').disabled = true;
    document.getElementById('add_file').disabled = true;
    
    navigator.geolocation.getCurrentPosition(success, error, {
        enableHighAccuracy: true
    });
});


// создаем локальные переменные для карты и маркера
// каждый модуль имеет собственное пространство имен
let map = null;
let marker = null;

// функция принимает позицию - массив с широтой и долготой
// и сообщение, отображаемое над маркером (tooltip)
function getMap(position, tooltip, flag) {
    // если карта не была инициализирована
    if (map === null) {
        // второй аргумент, принимаемый методом setView - это масштаб (zoom)
        map = L.map('map').setView(position, 12);
        
    } else return

    // что-то типа рекламы
    // без этого карта работать не будет
    /*
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    */
    
    googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3']
    }).addTo(map);
    
    response = fetch('/geolocation/get', {
        method: 'GET'
    })
        .then(response => response.json())
        .then(result => get(result));

    function get(result) {
        for (let key in result) {
            if (result[key][4]) {
                L.marker([result[key][2], result[key][3]]).addTo(map).bindPopup('<div class="w3-center"><strong>' + result[key][7] + '</strong></div><div class="w3-center">' + result[key][6] + '</div><p class="message" style="width: 130px">' + result[key][1] + '</p><div><a href="/geolocation/file/' + result[key][0] + '" target="_blank"><img src="/geolocation/file/' + result[key][0] + '" width="130px" height="100%"/></a></div>').openPopup();
            } else {
                L.marker([result[key][2], result[key][3]]).addTo(map).bindPopup('<div class="w3-center"><strong>' + result[key][7] + '</strong></div><div class="w3-center">' + result[key][6] + '</div><p class="message" style="width: 130px">' + result[key][1] + '</p>').openPopup();
            }
        }
        
        if (flag) {
            L.marker(position).addTo(map).bindPopup(tooltip).openPopup();
        }
    };
}

function success({ coords }) {
    const { latitude, longitude } = coords;
    const currentPosition = [latitude, longitude];
    // вызываем функцию, передавая ей текущую позицию и сообщение
    getMap(currentPosition, 'Вы здесь!', true);
    
    document.getElementById('text').disabled = false;
    document.getElementById('share').disabled = false;
    document.getElementById('add_file').disabled = false;
    
    document.getElementById('share').onclick = () => {
        document.getElementById('text').disabled = true;
        document.getElementById('share').disabled = true;
        document.getElementById('add_file').disabled = true;
        document.getElementById('info').innerText = 'сообщение отправляется!';
        
        let formData = new FormData();
        formData.append('latitude', latitude);
        formData.append('longitude', longitude);
        formData.append('text', document.getElementById('text').value);
        
        if (document.getElementById('file').value) {
            formData.append('file', file.files[0]);
            formData.append('file_size', document.getElementById('file_size').value);
        };
        
        response = fetch('/geolocation/add', {
            method: 'POST',
            body: formData
        })
            .then(response => response.text())
            .then(result => get(result));
        
        function get(result) {
            document.getElementById('info').innerText = result;
        }
    };
}

function error({ message }) {
    getMap([56.01, 92.99], 'Вы здесь!', false);
    document.getElementById('info').innerText = 'включите определение местоположения, разрешите геолокацию и перезагрузите страницу, чтобы увидеть метку где находитесь и поделиться местоположением с комментарием и фото.';
}

function addFile(event) {
    event.preventDefault();
    event.stopImmediatePropagation();

    let f = document.getElementById('file');
    f.click();
    f.onchange = function(event) {
        document.getElementById('file_size').value = file.files[0].size;
        document.getElementById('info').innerText = file.files[0].name
    }
}
/*
navigator.geolocation.getCurrentPosition(success, error, {

    enableHighAccuracy: true
});
*/

