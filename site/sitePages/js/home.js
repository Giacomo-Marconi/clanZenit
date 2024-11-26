
let data = [];
const url = "http://127.0.0.1"
const port = ":5000"
function init()  {
    fetch(url+port+'/getData')
        .then(response => {
            if (!response.ok) {
                throw new Error('error getData');
            }
            return response.json();
        })
        .then(json => {
            for (let i = 0; i < json.length; i++) {
                data.push(createTriPair(json[i].name, json[i].role_name, json[i].id));
            }
            addCombination();
        })
        .catch(error => {
            console.error('error function: combination person-role:', error);
        });
}

function createTriPair(name, role, id) {
    return new TriPair(name, role, id);
}


function addCombination() {
    for (let i = 0; i < data.length; i++) {
        document.getElementById('people').appendChild(createCombination(data[i]));
    }
}

function createCombination(combin) {
    //console.log(combin);
    let container = document.createElement('div');
    container.className = 'riga';


    let user = document.createElement('div');
    user.className = 'persona user-name';
    if(combin.first == 'Drago'){
        console.log('Drago');
        user.onclick = function() {
            drago()
        }
    }
    let p = document.createElement('p');
    p.innerHTML = combin.first;
    p.className = 'nome';

    user.appendChild(p);

    let role = document.createElement('div');
    role.className = 'persona user-role';

    let r = document.createElement('p');
    r.innerHTML = combin.second;
    r.className = 'nome';

    role.appendChild(r);

    container.appendChild(user);
    container.appendChild(role);

    return container;
}

function drago() {
    window.location.href = '/img/qwerty.jpeg';
    //console.log('dr');
}



class TriPair {
    constructor(first, second, tird) {
        this.first = first;
        this.second = second;
        this.tird = tird;
    }
}