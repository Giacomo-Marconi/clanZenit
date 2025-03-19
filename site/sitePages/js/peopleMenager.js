const url = "http://127.0.0.1"
const port = ":5000"
let users;
const token = localStorage.getItem('token');

function init()  {
    const add = document.getElementById('people');
    add.innerHTML = "";
    fetch(url+port+'/getPerson', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Barer " + token
        }})
        .then(response => {
            if(response.status == 403){
                window.location.href = url + port + '/login';
                localStorage.setItem('last', "person");
                alert("non loggato1");
                return;
            }
            if(response.status == 401){
                window.location.href = url + '/';
                alert("Accesso solo agli admin");
            }
            if (!response.ok) {
                throw new Error('error getPerson');
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

    fetch(url+port+'/removePerson', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Barer " + token
        },
        body: JSON.stringify({
            id: id
        })
    })
        .then(response => {
            if(response.status == 403){
                window.location.href = url + port + '/login';
                localStorage.setItem('last', "person");
                alert("non loggato2");
                return;
            }
            if(response.status == 401){
                window.location.href = url + '/';
                alert("Accesso solo agli admin");
            }
            if (!response.ok) {
                console.log('error removePerson');
            }
            return response.json();
        });
}


function createBremove(id) {
    let bremove = document.createElement('button')
    // bremove.className="input-item interno";
    bremove.innerHTML="remove";
    bremove.onclick = function() {
        remove(id);
        document.getElementById('form' + id).remove();
    }
    return bremove;
}

async function getRoles() {
    let roles;
    await fetch(url+port+'/getRole', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Barer " + token
        }
    })
    .then(response => {
        if(response.status == 403){
            window.location.href = url + port + '/login';
            localStorage.setItem('last', "person");
            alert("non loggato3");
            return;
        }
        if(response.status == 401){
            window.location.href = url + '/';
            alert("Accesso solo agli admin");
        }
        if (!response.ok) {
            console.log('error getRole');
        }
        return response.json();
    })
    .then(data => {
        roles = data;
    })
    return roles;
}

 function adminPeople(id, roles, id_role) {
    const div = document.createElement('div');
    div.classList.add('admin-people');
    const button = createBremove(id);
    const select = document.createElement('select');
    select.dataset.id = id;
    
    const option = document.createElement('option');
    option.value = null;
    option.innerHTML = "nessun ruolo";
    select.appendChild(option);
    
    roles.map((role) => {
        const option = document.createElement('option');
        option.value = role.id;
        option.innerHTML = role.role_name;
        select.appendChild(option);
    });

    select.value = id_role;
    div.appendChild(select);
    div.appendChild(button);


    select.addEventListener('change', (event) => {
        const personId = event.target.dataset.id;
        const roleId = event.target.value;

        fetch (url+port+'/setRole', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Barer " + token
            },
            body: JSON.stringify({
                personId: personId,
                roleId: roleId
            })
        })
            .then(response => {
                if(response.status == 403){
                    window.location.href = url + port + '/login';
                    localStorage.setItem('last', "person");
                    alert("non loggato4");
                    return;
                }
                if(response.status == 401){
                    window.location.href = url + '/';
                    alert("Accesso solo agli admin");
                }
                if (!response.ok) {
                    throw new Error('error setRole');
                }
                return response.json();
            })
            .then(data => {
                window.location.reload();
            });
    });
    return div;
}


 function createPerson(name, idd, roles, idRole) {
    let classe = "riga";
    let persona = Object.assign(document.createElement('div'), {
        id: 'form' + idd,
        className: classe,
    });


    let p = Object.assign(document.createElement('p'), {
        className: 'nome',
        innerText: name,
    });

    let bremove =  adminPeople(idd, roles, idRole);

    //persona.appendChild(hinput);
    persona.appendChild(p);
    persona.appendChild(bremove);

    return persona;
}

async function addPerson(){
    const roles = await getRoles();
    for (let i = 0; i < users.length; i++) {
        document.getElementById('people').appendChild(createPerson(users[i].name, users[i].id, roles, users[i].role));
    }
}


function newPerson() {
    const name = document.getElementById('input-name').value;
    fetch(url+port+'/addPerson', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Barer " + token
        },
        body: JSON.stringify({
            name: name
        })
    })
        .then(response => {
            if(response.status == 403){
                window.location.href = url + port + '/login';
                localStorage.setItem('last', "person");
                alert("non loggato5");
                return;
            }
            if(response.status == 401){
                window.location.href = url + '/';
                alert("Accesso solo agli admin");
            }
            if (!response.ok) {
                console.log('error addPerson');
            }
            //relaod page
            init();
            name.value = "";
        });
}


function shuffle() {
    const confirm = window.confirm("confermi shuffle?");
    if(confirm){
        fetch(url+port+'/shuffle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Barer " + token
            }
        })
            .then(response => {
                if(response.status == 403){
                    window.location.href = url + port + '/login';
                    localStorage.setItem('last', "person");
                    alert("non loggato6");
                    return;
                }
                if(response.status == 401){
                    window.location.href = url + '/';
                    alert("Accesso solo agli admin");
                }
                if (!response.ok) {
                    alert("error shuffle");
                    console.log('error shuffle');
                }
                init();
            });
    }
}