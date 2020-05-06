<?php

define('ROSTER_BATH_PATH', '../../../jmri-data/');

function outputAsJson($data){
    header('Content-type: application/json');
    $json = json_encode($data);
    // Filter out null fields. Unfortunately array_filter() only works on single-dimensional arrays so we have to use this jank.
    echo preg_replace('/,\s*"[^"]+":null|"[^"]+":null,?/', '', $json);
}
?>