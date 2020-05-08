<?php
include_once('api_base.php');

function outputImageAsJpg($image){
    header('Content-type: image/jpeg');
    imagejpeg($image, NULL, 80);
}

if(!isset($_GET['locomotive_id'])){
    http_response_code(422);
    outputAsJson(array('error' => 'locomotive_id not provided.'));
    die();
}

include_once('../../common/loader.php');

define('IMAGE_EXTENSION_JPG', 'jpg');
define('IMAGE_EXTENSION_PNG', 'png');
define('MAX_WIDTH', 6000);

$loader = new Loader(ROSTER_BASE_PATH);
$locomotive = $loader->loadLocomotive($_GET['locomotive_id']);
$supportedImageExtensions = array(IMAGE_EXTENSION_JPG, IMAGE_EXTENSION_PNG);

if($locomotive==null){
    http_response_code(404);
    outputAsJson(array('error:' => 'Locomotive with ID '.$_GET['locomotive_id'].' not found.'));
    die();
}

if(!isSetAndNotEmpty($locomotive->imageFilePath)){
    http_response_code(404);
    outputAsJson(array('error:' => 'Locomotive with ID '.$_GET['locomotive_id'].' has no roster image.'));
    die();
}

# Check if the image file type is supported.
$imageExtension = pathinfo($locomotive->imageFilePath, PATHINFO_EXTENSION);
if(!in_array($imageExtension, $supportedImageExtensions)){
    http_response_code(415);
    outputAsJson(array('error:' => 'Locomotive with ID '.$_GET['locomotive_id'].' has an image type that is not supported.'));
    die();
}

# If we reach here, there is an image we can work with.
$startTimestamp = getCurrentTimeMs();

$image;
switch($imageExtension){
    case IMAGE_EXTENSION_JPG:
        $image = imagecreatefromjpeg(ROSTER_BASE_PATH . '/' . $locomotive->imageFilePath);
        break;
    case IMAGE_EXTENSION_PNG:
        $image = imagecreatefrompng(ROSTER_BASE_PATH . '/' . $locomotive->imageFilePath);
        break;
}
header('API-Image-Load-Time: ' . (getCurrentTimeMs() - $startTimestamp) . 'ms');

# The image is now loaded.
$imageWidth = imagesx($image);
$imageHeight = imagesy($image);

# A desired image width has been specified.
if(isset($_GET['width'])){
    # Check the requested width isn't greater than the maximum allowed width.
    if($_GET['width'] > MAX_WIDTH){
        http_response_code(404);
        outputAsJson(array('error:' => 'Request width '.$_GET['width'].' is greater than max-width ('.MAX_WIDTH.').'));
        die();
    }
    $newWidth = $_GET['width'];
    # Scale the height too, to preserve the image's aspect ratio.
    $newHeight = $imageHeight * ($newWidth / $imageWidth);
    $startTimestamp = getCurrentTimeMs();
    $resizedImage = imagecreatetruecolor($newWidth, $newHeight);
    imagecopyresampled($resizedImage, $image, 0, 0, 0, 0, $newWidth, $newHeight, $imageWidth, $imageHeight);
    header('API-Image-Resize-Time: ' . (getCurrentTimeMs() - $startTimestamp) . 'ms');
    outputImageAsJpg($resizedImage);
}
# No width specified, so simply output the image "as is".
else{
    outputImageAsJpg($image);
}
?>