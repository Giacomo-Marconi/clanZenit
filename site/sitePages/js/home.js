
let data = [];
const url = "http://127.0.0.1:5000"
function init()  {
    fetch(url+'/getData')
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
    /*user.onclick = function() {
        test(combin.tird)
    }*/
    if(combin.first == 'Drago'){
        console.log('Drago');
        user.onclick = function() {
            drago()
        }
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



function test(n) {
    fetch('/php/cookies.php?id=' + n)
}

function drago() {
    window.location.href = '/img/qwerty.jpeg';
    //console.log('dr');
}



function checkDate() {
    fetch('php/date/updateRuoli.php')
    .then(response => {
        if (!response.ok) {
            throw new Error('error updateRuoli.php');
        }
        return response.json();
    })
    .then(json => {       
        /*if(json.diff < 7) {
            delLoadBar();
        }else{
            //must recalocalre role
            ///updateDate(); ogni volta che ricalcolo i ruoli
            insLoadBar();
        }*/
    })
    .catch(error => {console.error('error function: checkDate:', error)});
}



class TriPair {
    constructor(first, second, tird) {
        this.first = first;
        this.second = second;
        this.tird = tird;
    }
}