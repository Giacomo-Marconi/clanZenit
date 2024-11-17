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

if($_SERVER['REQUEST_METHOD'!='GET']){
    http_response_code(405);
    exit("Method not allowed");
}


if(isset($_GET['getPersone'])){
    $sql = "SELECT id, name FROM user ORDER BY role desc";
    $result = $conn->query($sql);
    if($result->num_rows > 0){
        $rows = array();
        while($row = $result->fetch_assoc()){
            $rows[] = $row;
        }
        echo json_encode($rows);
    }
}

if(isset($_GET['getRuoli'])){
    $sql = "SELECT * FROM role ORDER BY id desc";
    $result = $conn->query($sql);
    if($result->num_rows > 0){
        $rows = array();
        while($row = $result->fetch_assoc()){
            $rows[] = $row;
        }
        echo json_encode($rows);
    }
}

if(isset($_GET['getRuoliPersone'])){
    $sql = "SELECT u.id, u.name, r.role_name FROM user u, role r where u.role = r.id union select u.id, u.name, 'Fortunello' FROM user u where role is null";
    $result = $conn->query($sql);
    if($result->num_rows > 0){
        $rows = array();
        while($row = $result->fetch_assoc()){
            $rows[] = $row;
        }
        echo json_encode($rows);
    }
}




?>