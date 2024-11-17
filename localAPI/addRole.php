<?php

//connect to the database
$servername = "localhost";
$username = getenv('dbUser');
$password = getenv('dbPassword');
$dbname = "clanZenit2";


// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
if($conn->connect_error){
    //send error 522
    http_response_code(522);
    exit("Connection failed: " . $conn->connect_error);
}


if($_SERVER['REQUEST_METHOD'!='POST']){
    http_response_code(405);
    exit("Method not allowed");
}

if(isset($_POST['roleName'])){
    $roleName = $_POST['roleName'];
    $stm = $conn->prepare("INSERT INTO role (role_name) VALUES (?)");
    $stm->bind_param("s", $roleName);
    if($stm->execute()){
        http_response_code(201);
        exit("Role added");
    }
    else{
        http_response_code(500);
        exit("Error: " . $sql . "<br>" . $conn->error);
    }
}

?>