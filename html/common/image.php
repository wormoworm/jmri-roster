<?php

define('IMAGE_EXTENSION_JPG', 'jpg');
define('IMAGE_EXTENSION_PNG', 'png');
define('MAX_WIDTH', 6000);

function loadImage($imagePath){
    $startTimestamp = getCurrentTimeMs();
    $imageExtension = pathinfo($imagePath, PATHINFO_EXTENSION);
    $image = null;
    switch($imageExtension){
        case IMAGE_EXTENSION_JPG:
            $image = imagecreatefromjpeg($imagePath);
            break;
        case IMAGE_EXTENSION_PNG:
            $image = imagecreatefrompng($imagePath);
            break;
    }
    header('API-Image-Load-Time: ' . (getCurrentTimeMs() - $startTimestamp) . 'ms');
    return $image;
}

function getImageDimensions($imagePath, $desiredWidth = null){
    $imageDimensions = getimagesize($imagePath);
    $imageWidth = $imageDimensions[0];
    $imageHeight = $imageDimensions[1];
    if($desiredWidth!=null){
        $imageHeight = $imageHeight * ($desiredWidth / $imageWidth);
        $imageWidth = $desiredWidth;
    }
    return array('width' => $imageWidth, 'height' => $imageHeight);
}
?>