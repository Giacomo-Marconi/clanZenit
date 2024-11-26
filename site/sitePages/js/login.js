const url = "http://127.0.0.1"
const port = ":5000"
function login() {
    const user = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch(url+port+'/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user: user, password: password }),
    })
    .then((response) => {
        if(response.status == 200){
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
        window.location.href = url + '/person';
    });
}
