<?php
// Include the database configuration file
require_once 'database.php';

// Check if the keyword is submitted
if (isset($_GET['keyword'])) {
  $keyword = $_GET['keyword'];

  // Fetch search results from the database
  $sql = "SELECT * FROM posts WHERE title LIKE '%$keyword%' OR content LIKE '%$keyword%'";
  $result = mysqli_query($conn, $sql);

  // Loop through the search results and display them
  while ($row = mysqli_fetch_assoc($result)) {
    $title = $row['title'];
    $content = $row['content'];

    echo '<div class="card">';
    echo '<div class="card-body">';
    echo '<h5 class="card-title">' . $title . '</h5>';
    echo '<p class="card-text">' . $content . '</p>';
    echo '</div>';
    echo '</div>';
  }

  // If no search results found
  if (mysqli_num_rows($result) === 0) {
    echo '<p>No search results found.</p>';
  }
}
?>
