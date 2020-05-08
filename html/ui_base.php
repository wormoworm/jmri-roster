<?php

define('ROSTER_BATH_PATH', '../jmri-data/');

function getFriendlyDate($timestamp){
    return date('jS F Y', $timestamp);
}

function getFriendlyTime($timestamp){
    return date('H:i', $timestamp);
}

function displayFooter(){
    echo '';
}
?>