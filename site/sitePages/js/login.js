function login1() {
    const user = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/login1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user: user, password: password }),
    })
        .then((response) => {
            if (response.ok) {
                return response.json();
            }else{
                alert("username o password incorrette");
            }
        })
        .then((data) => {
            localStorage.setItem('token', data.token);
            //window.location.href = 'http://localhost:5000/home';
        });
}

function login() {
    const user = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user: user, password: password }),
    })
    .then((response) => {
        if(response.status == 200){
            alert("Login riuscito");
            return response.json();
        }
        else if(response.status == 401){
            alert("Username o password incorretti");
            return response.json();
        }
        else{
            alert("Error");
            return {'token': ''};
        }
    })
    .then((data) => {
        localStorage.setItem('token', data.token);
    });
}
