<!DOCTYPE html>
<html>
<head>
    <title>GET Example</title>
</head>
<body>

<?php
// Check if the 'name' and 'age' query parameters exist
if (isset($_GET['name']) && isset($_GET['age'])) {
    $name = htmlspecialchars($_GET['name']); // Sanitize input
    $age = htmlspecialchars($_GET['age']);   // Sanitize input

    // Display the values
    echo "<h1>Welcome, " . $name . "!</h1>";
    echo "<p>Your age is: " . $age . "</p>";
} else {
    echo "<h1>Please provide both a name and an age.</h1>";
}
?>

</body>
</html>
