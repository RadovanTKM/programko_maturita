<?php
// Proměnné pro spojení s databází.

$dbhost = "dbs.spskladno.cz";
$dbuser = "student13";
$dbpass = "spsnet";
$dbname = "vyuka13"; 

// Připojení k databázi.
$conn = new mysqli($dbhost, $dbuser, $dbpass, $dbname);

// Kontrola připojení k databázi.
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
