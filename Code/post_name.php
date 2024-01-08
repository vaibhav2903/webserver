<!-- PHP Script to handle POST data -->
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    parse_str($_SERVER['POST_DATA'], $_POST);  // Use the POST_DATA environment variable

    $name = isset($_POST["name"]) ? $_POST["name"] : "undefined";
    // Collect value of input field
    echo "Name: " . $name . "<br>";
}
?>