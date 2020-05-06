<?php
ini_set('display_errors', 1);

include_once('api_base.php');
include_once('../common/loader.php');

$loader = new Loader(ROSTER_BATH_PATH);
$locomotives = $loader->loadRoster();
outputAsJson($locomotives);

?>