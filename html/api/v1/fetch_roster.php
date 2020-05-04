<?php
ini_set('display_errors', 1);
include_once('src/locomotive.php');
include_once('src/utils.php');

$startTime = getCurrentTimeMs();

$xml = simplexml_load_file('../../../jmri-data/roster.xml');
$roster = $xml->children()[0];

$locomotives = [];

foreach($roster as $locomotiveXML){
    $locomotive = processLocomotiveFromXML($locomotiveXML);
    $locomotives[] = $locomotive;
}

header('Content-type: application/json');
$json = json_encode($locomotives);
// Filter out null fields from the Locomotive objects. Unfortunately array_filter() only works on single-dimensional arrays so we have to use this jank.
echo preg_replace('/,\s*"[^"]+":null|"[^"]+":null,?/', '', $json);

$endTime = getCurrentTimeMs();
error_log("Loaded " . (sizeof($locomotives)) . " locomotives in " . ($endTime - $startTime) . "ms");
?>