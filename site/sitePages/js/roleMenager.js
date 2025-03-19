let role;
const url = "http://127.0.0.1"
const port = ":5000"
const token = localStorage.getItem('token');

function init()  {
    const add = document.getElementById('people');
    add.innerHTML = "";
    fetch(url+port+'/getRole',{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Barer " + token
        }
    })
        .then(response => {
            if(response.status == 403){
                window.location.href = url + port + '/login';
                localStorage.setItem('last', "role");
                alert("non loggato");
                return;
            }
            if (!response.ok) {
                throw new Error('error getRole');
            }
            return response.json();
        })
        .then(data => {
            role = data;
            addRole();
        })
        .catch(error => {
            console.error('error function: readRole:', error);
        });
}


function createHiddenInout(id) {
    let input = document.createElement('input');
    input.id="hiddenR"+id;
    input.type = "hidden";
    input.name = "id";
    input.value = id;
    return input;
}


function remove(id) {
    fetch(url+port+'/removeRole', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Barer " + token
        },
        body: JSON.stringify({
            roleId: id
        })
    })
        .then(response => {
            if(response.status == 403){
                alert("non loggato");
                window.location.href = url + port + '/login';
                localStorage.setItem('last', "role");
                return;
            }
            if(response.status == 402){
                alert("qs ruolo ha dei membri");
                return;
            }
            if (!response.ok) {
                console.log('error removeRole');
            }
            return response.json();
        });    
}


function createBremove(id) {
    let bremove = document.createElement('button')
    bremove.className="butt-remove";
    bremove.value="remove";
    bremove.innerHTML="remove";
    bremove.onclick = function() {
        remove(id);
        document.getElementById('formR' + id).remove();
    }
    return bremove;
}

function createRole(name, id) {
    let persona = Object.assign(document.createElement('div'), {
        id: 'formR' + id,
        className: 'riga',
        //action: 'php/ruoli/removeRole.php',
        //method: 'POST',
    });

    //let hinput = createHiddenInout(id);

    let p = Object.assign(document.createElement('p'), {
        className: 'nome',
        innerText: name,
    });

    let bremove = createBremove(id);

    persona.appendChild(p);
    persona.appendChild(bremove);

    return persona;
}

function addRole(){
    for (let i = 0; i < role.length; i++) {
        document.getElementById('people').appendChild(createRole(role[i].role_name, role[i].id));
    }
}


function newRole(params) {
    const roleName = document.getElementById('role-name').value;
    if (roleName === '') {
        alert('Inserisci un nome');
        return;
    }
    fetch(url+port+'/addRole', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Barer " + token
        },
        body: JSON.stringify({
            roleName: roleName
        })
    })
        .then(response => {
            if(response.status == 403){
                alert("non loggato");
                window.location.href = url + port + '/login';
                localStorage.setItem('last', "role");
                return;
            }
            if (!response.ok) {
                console.log('error addRole');
            }
            //relaod page
            init();
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
                    alert("non loggato");
                    window.location.href = url + port + '/login';
                    localStorage.setItem('last', "role");
                    return;
                }
                if (!response.ok) {
                    alert("error shuffle");
                    console.log('error shuffle');
                }
                init();
            });
    }
}