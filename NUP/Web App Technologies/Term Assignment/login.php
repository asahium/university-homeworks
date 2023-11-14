<?php
// Include the database configuration and functions files
require_once 'database.php';
require_once 'functions.php';

// Check if the form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  // Retrieve the submitted username and password
  $username = $_POST['username'];
  $password = $_POST['password'];

  // Validate the login credentials
  if (validateLogin($username, $password)) {
    // Valid login, redirect to the home page or user panel
    header('Location: index.html'); // Update the URL as per your project structure
    exit();
  } else {
    // Invalid login, display an error message
    $error = 'Invalid username or password';
  }
}
?>

<!DOCTYPE html>
<html>
<head>
  <title>Login</title>
  <!-- Include Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <!-- Include custom CSS -->
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <h1>Login</h1>
    <?php if (isset($error)): ?>
      <div class="alert alert-danger"><?php echo $error; ?></div>
    <?php endif; ?>
    <form method="POST" action="login.php">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" class="form-control" id="username" name="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" class="form-control" id="password" name="password" required>
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  </div>

  <!-- Include Bootstrap JS and jQuery -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.min.js"></script>
</body>
</html>
