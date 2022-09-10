<?php

header('Content-Type: application/json');

$data = [
  // use time since 19xx to generate a random integer
   'viewCount' => (time() % 1000) * 3
];

// return JSON dictionary
echo json_encode($data);

?>
