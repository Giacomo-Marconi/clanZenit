const url = "http://127.0.0.1:5000"
let users;
const token = localStorage.getItem('token');
function init()  {
    const add = document.getElementById('people');
    add.innerHTML = "";
    fetch(url+'/getPerson', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        }})
        .then(response => {
            if(response.status == 401){
                alert("non loggato");
                window.location.href = url + '/login';
                return;
            }
            if (!response.ok) {
                throw new Error('error getgetPerson');
            }
            return response.json();
        })
        .then(data => {
            users = data;
            addPerson();
        })
        .catch(error => {
            console.error('error function: readPeople:', error);
        });
}

function remove(id) {
    const data = new FormData();
    data.append('id', id);

    fetch(url+'/removePerson', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        },
        body: JSON.stringify({
            id: id
        })
    })
        .then(response => {
            if(response.status == 401){
                alert("non loggato");
                window.location.href = url + '/login';
                return;
            }
            if (!response.ok) {
                console.log('error removePerson');
            }
            return response.json();
        });
    //console.log("rimosso", id);
}

function changeAdmin(id) {
    let form = document.getElementById('form' + id);
    let h = document.getElementById('hidden' + id);
    h.value = 10000+parseInt(h.value);

    form.submit();
}


function createBremove(id) {
    let bremove = document.createElement('button')
    bremove.className="input-item interno";
    bremove.innerHTML="remove";
    bremove.onclick = function() {
        remove(id);
        document.getElementById('form' + id).remove();
    }
    return bremove;
}

function createHiddenInout(id) {
    let input = document.createElement('input');
    input.id="hidden"+id;
    input.type = "hidden";
    input.name = "id";
    input.value = id;
    return input;
}


function createPerson(name, idd) {
    let classe = "persona";
    let persona = Object.assign(document.createElement('div'), {
        id: 'form' + idd,
        className: classe,
        //action: '/php/persone/removePerson.php',
        //method: 'POST',
    });

    //let hinput = createHiddenInout(idd);

    let p = Object.assign(document.createElement('p'), {
        className: 'nome',
        innerText: name,
    });

    let bremove = createBremove(idd);

    //persona.appendChild(hinput);
    persona.appendChild(p);
    persona.appendChild(bremove);

    return persona;
}

function addPerson(){
    for (let i = 0; i < users.length; i++) {
        document.getElementById('people').appendChild(createPerson(users[i].name, users[i].id));
    }
}


function newPerson() {
    const name = document.getElementById('input-name').value;
    fetch(url+'/addPerson', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        },
        body: JSON.stringify({
            name: name
        })
    })
        .then(response => {
            if(response.status == 401){
                alert("non loggato");
                window.location.href = url + '/login';
                return;
            }
            if (!response.ok) {
                console.log('error addPerson');
            }
            //relaod page
            init();
            name.value = "";
        });
}