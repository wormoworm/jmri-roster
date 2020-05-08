<?php

if(!isset($_GET['locomotive_id'])){
    http_response_code(422);
    echo 'Error: locomotive_id not provided';
    die();
}

include('ui_base.php');
include_once('common/loader.php');

$loader = new Loader(ROSTER_BATH_PATH);
$locomotive = $loader -> loadLocomotive($_GET['locomotive_id']);
if($locomotive==null){
    http_response_code(404);
    echo 'Error: Locomotive with ID '.$_GET['locomotive_id'].' not found';
    die();
}

# If we reach here, we have a locomotive's data to display.

# TODO Output a nice table with loco image.
echo 
'<html>
    <head>
        <title>'.$locomotive->id.'</title>
    </head>
</html>';
print_r($locomotive);
?>