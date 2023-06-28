<?php
function kilometers_to_miles($kilometers = 0)
{
$miles_scale = 0.62;
return $kilometers * $miles_scale;
}
echo kilometers_to_miles(100);
?>

