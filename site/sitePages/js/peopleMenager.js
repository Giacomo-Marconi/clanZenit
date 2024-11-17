const url = "http://127.0.0.1:5000"
let users;
function init()  {
    fetch(url+'/getPerson')
        .then(response => {
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
    fetch(url+'/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'id=' + encodeURIComponent(id)
    })
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


