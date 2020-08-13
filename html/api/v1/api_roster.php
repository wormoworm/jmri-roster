<?php
ini_set('display_errors', 1);

include_once('api_base.php');
include_once('../../common/loader.php');

$loader = new Loader(ROSTER_BASE_PATH);
$roster = $loader->loadRoster();
outputAsJson($roster);

?>