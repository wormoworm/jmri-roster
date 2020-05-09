<?php
ini_set('display_errors', '1');

$rewritesAvailable = false;

$imageWidth = 700;

if(!isset($_GET['locomotive_id'])){
    http_response_code(422);
    echo 'Error: locomotive_id not provided';
    die();
}

include('ui_base.php');
include_once('common/loader.php');

function getPageTitle($locomotive){
    return $locomotive->id;
}

function outputField($name, $value){
    echo '
    <p class="fieldName">'.$name.'</p>
    <p class="fieldValue">'.$value.'</p>';
}

$loader = new Loader(ROSTER_BATH_PATH);
$locomotive = $loader -> loadLocomotive($_GET['locomotive_id']);
if($locomotive==null){
    http_response_code(404);
    echo 'Error: Locomotive with ID '.$_GET['locomotive_id'].' not found';
    die();
}
?>

<html>
    <head>
        <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
        <title><?php echo getPageTitle($locomotive); ?></title>
    </head>
    <body>
        <h1 id="title"><?php echo getPageTitle($locomotive); ?></h1>
        <?php
        $imagePath = $rewritesAvailable ? '../api/v1/locomotive/'.$locomotive->id.'/image/'.$imageWidth : '/api/v1/api_locomotive_image.php?locomotive_id='.$locomotive->id.'&width='.$imageWidth;
        if(isset($locomotive->imageFilePath)) echo '<img id="image" src="'.$imagePath.'"/>';
        if(isSetAndNotEmpty($locomotive->manufacturer)) outputField('Manufacturer', $locomotive->manufacturer);
        if(isSetAndNotEmpty($locomotive->model)) outputField('Model', $locomotive->model);
        if(isset($locomotive->comment)) echo '<p id="comment" class="body">'.$locomotive->comment.'</p>';
        ?>
    </body>
</html>