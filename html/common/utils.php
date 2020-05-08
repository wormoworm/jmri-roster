<?php
// Commonly-used util functions

function getCurrentTimeMs(){
    return round(microtime(true) * 1000);
}

function isSetAndNotEmpty($value){
    return isset($value) && $value != "";
}

?>