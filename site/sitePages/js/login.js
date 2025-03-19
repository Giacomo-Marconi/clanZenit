const url = "http://127.0.0.1"
const port = ":5000"

function getTokenFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('token');
}

const token = getTokenFromUrl();
console.log(token);
    
if (token) {
    localStorage.setItem('token', token);
    const last = localStorage.getItem('last');

    if (last && (last == "person" || last == "role")) {
       window.location.href = url + '/' + last + ".html";
    }
    else{
        window.location.href = "/";
    }
}