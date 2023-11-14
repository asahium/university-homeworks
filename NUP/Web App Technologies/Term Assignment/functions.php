<?php
// Validate user login
function validateLogin($username, $password) {
  global $conn;

  $username = mysqli_real_escape_string($conn, $username);
  $password = mysqli_real_escape_string($conn, $password);

  $sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
  $result = mysqli_query($conn, $sql);

  if (mysqli_num_rows($result) == 1) {
    return true; // Valid login
  } else {
    return false; // Invalid login
  }
}
