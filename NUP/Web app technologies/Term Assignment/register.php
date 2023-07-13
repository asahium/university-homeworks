<?php
// Include the database configuration file
require_once 'database.php';

// Check if the form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  // Retrieve the submitted user data
  $username = $_POST['username'];
  $email = $_POST['email'];
  $password = $_POST['password'];

  // Insert the user data into the database
  $sql = "INSERT INTO users (username, email, password) VALUES ('$username', '$email', '$password')";
  if (mysqli_query($conn, $sql)) {
    // Registration successful, redirect to the login page
    header('Location: login.html'); // Update the URL as per your project structure
    exit();
  } else {
    // Error occurred, display an error message
    $error = 'Error: ' . mysqli_error($conn);
  }
}
?>

<!DOCTYPE html>
<html>
<head>
  <title>Registration</title>
  <!-- Include Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <!-- Include custom CSS -->
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <h1>Registration</h1>
    <?php if (isset($error)): ?>
      <div class="alert alert-danger"><?php echo $error; ?></div>
    <?php endif; ?>
    <form method="POST" action="register.php">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" class="form-control" id="username" name="username" required>
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" class="form-control" id="email" name="email" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" class="form-control" id="password" name="password" required>
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
  </div>

  <!-- Include Bootstrap JS and jQuery -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.min.js"></script>
</body>
</html>
