<?php
include_once('api_base.php');

if(!isset($_GET['locomotive_id'])){
    http_response_code(422);
    outputAsJson(array('error' => 'locomotive_id not provided'));
    die();
}

include_once('../../common/loader.php');

$loader = new Loader(ROSTER_BASE_PATH);
$rosterEntry = $loader->loadRosterEntry($_GET['locomotive_id']);

if($rosterEntry==null){
    http_response_code(404);
    outputAsJson(array('error:' => 'Locomotive with ID '.$_GET['locomotive_id'].' not found'));
    die();
}

# If we reach here, we have a locomotive's data to display.
outputAsJson($rosterEntry);
?>