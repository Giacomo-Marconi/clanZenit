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

if(isset($_POST['role']) && isset($_POST['name'])){
    $role = $_POST['role'];
    $name = $_POST['name'];
    $stm = $conn->prepare("INSERT INTO user (name, role) VALUES (?, ?)");
    $stm->bind_param("si", $name, $role);
    if($stm->execute()){
        http_response_code(201);
        exit("Person added");
    }
    else{
        http_response_code(500);
        exit("Error: " . $sql . "<br>" . $conn->error);
    }
}


if(isset($_POST['name'])){
    $name = $_POST['name'];
    $stm = $conn->prepare("INSERT INTO user (name) VALUES (%s)");
    $stm->bind_param("s", $name);
    if($stm->execute()){
        http_response_code(201);
        exit("Person added");
    }
    else{
        http_response_code(500);
        exit("Error: " . $sql . "<br>" . $conn->error);
    }
}

?>