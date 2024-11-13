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

function checkDate() {
    fetch('php/py/getDate.php')
    .then(response => {
        if (!response.ok) {
            throw new Error('error getDate.php');
        }
        return response.json();
    })
    .then(json => {       
        if(json.diff < 7) {
            delLoadBar();
        }else{
            //must recalocalre role
            ///updateDate(); ogni volta che ricalcolo i ruoli
            insLoadBar();
        }
    })
    .catch(error => {console.error('error function: checkDate:', error)});
}


function insLoadBar() {
    let body = document.getElementById('body');
    let blur = document.createElement('div');
    blur.id = 'del1';
    blur.className = 'blur';

    let load = document.createElement('div');
    load.id = 'del2';
    load.className = 'div-load';

    let prbar = document.createElement('div');
    prbar.id = 'progressbar';
    prbar.className = 'progress';

    load.appendChild(prbar);

    body.appendChild(blur);
    body.appendChild(load);

    let progressBar = document.getElementById('progressbar');
    progressBar.addEventListener('animationend', delLoadBar);

}

function delLoadBar() {
    init();

    let pr1 = document.getElementById('del1');
    let pr2 = document.getElementById('del2');

    if(pr1 == null || pr2== null) return;

    pr1.parentNode.removeChild(pr1);
    pr2.parentNode.removeChild(pr2);
}

function remove(id) {
    fetch('/php/persone/removePerson.php', {
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
    let bremove = document.createElement('input')
    bremove.className="input-item interno";
    bremove.type="submit";
    bremove.value="remove";
    return bremove;
}


function createCheckbox(id, admin) {
    let checkbox = document.createElement('input');
    checkbox.className="checkb";
    checkbox.type="checkbox";
    checkbox.id="admin"+id;
    checkbox.onchange = function() {
        changeAdmin(id);
    };

    if(admin==1){
        checkbox.checked = true;
    }
    return checkbox;
}

function createHiddenInout(id) {
    let input = document.createElement('input');
    input.id="hidden"+id;
    input.type = "hidden";
    input.name = "id";
    input.value = id;
    return input;
}


function createPerson(name, idd, admin, superadmin) {
    let classe = "persona";
    if(superadmin==1){
        classe = "persona admin";
    }
    let persona = Object.assign(document.createElement('form'), {
        id: 'form' + idd,
        className: classe,
        action: '/php/persone/removePerson.php',
        method: 'POST',
    });

    let hinput = createHiddenInout(idd);

    let checkbox = createCheckbox(idd, admin);

    let p = Object.assign(document.createElement('p'), {
        className: 'nome',
        innerText: name,
    });

    let bremove = createBremove(idd);

    persona.appendChild(hinput);
    persona.appendChild(checkbox);
    persona.appendChild(p);
    persona.appendChild(bremove);

    return persona;
}

function addPerson(){
    for (let i = 0; i < users.length; i++) {
        document.getElementById('people').appendChild(createPerson(users[i].name, users[i].id, 0, 0));
    }
}


