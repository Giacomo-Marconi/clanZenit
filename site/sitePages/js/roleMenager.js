let role;
const url = "http://127.0.0.1:5000"
function init()  {
    fetch(url+'/getRole')
        .then(response => {
            if (!response.ok) {
                throw new Error('error getRole.php');
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


function createBremove(id) {
    let bremove = document.createElement('input')
    bremove.className="input-item interno";
    bremove.type="submit";
    bremove.value="remove";
    return bremove;
}

function createRole(name, id) {
    let persona = Object.assign(document.createElement('form'), {
        id: 'formR' + id,
        className: 'persona role',
        action: 'php/ruoli/removeRole.php',
        method: 'POST',
    });

    let hinput = createHiddenInout(id);

    let p = Object.assign(document.createElement('p'), {
        className: 'nome',
        innerText: name,
    });

    let bremove = createBremove(id);

    persona.appendChild(hinput);
    persona.appendChild(p);
    persona.appendChild(bremove);

    return persona;
}

function addRole(){
    for (let i = 0; i < role.length; i++) {
        document.getElementById('people').appendChild(createRole(role[i].role_name, role[i].id));
    }
}


