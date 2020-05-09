<?php
// Commonly-used util functions

function getCurrentTimeMs(){
    return round(microtime(true) * 1000);
}

function isSetAndNotEmpty($value){
    return isset($value) && $value != "";
}

function getFriendlyDate($timestamp){
    return date('jS F Y', $timestamp);
}

function getFriendlyTime($timestamp){
    return date('H:i', $timestamp);
}

function getFriendlyDuration($durationS){
    $hours = floor($durationS / 3600);
    $hoursRemainder = $durationS % 3600;
    $minutes = floor($hoursRemainder / 60);
    $seconds = $hoursRemainder % 60;
    if($hours > 0){
        $output = $hours.' hour';
        if($hours > 1) $output.='s';
        if($minutes > 0){
            $output.=' '.$minutes.' minute';
            if($minutes > 1) $output.='s';
        }
        return $output;
    }
    else if($minutes > 0){
        $output = $minutes.' minute';
        if($minutes > 1) $output.='s';
        if($seconds > 0){
            $output.=' '.$seconds.' second';
            if($seconds > 1) $output.='s';
        }
        return $output;
    }
    else if($seconds > 0){
        $output = $seconds.' second';
        if($seconds > 1) $output.='s';
        return $output;
    }
}

?>