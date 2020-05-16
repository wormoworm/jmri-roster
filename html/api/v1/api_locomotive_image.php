<?php
include_once('api_base.php');

// print_r(getallheaders());
// die();

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
include_once('../../common/image.php');

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

# Get the image file's modification time - we will use this for caching
$fileModificationTimestamp = filemtime(ROSTER_BASE_PATH . '/' . $locomotive->imageFilePath);
# Check this modification timestamp against the one provided by the browser, if supplied.
if(isset($_SERVER['HTTP_IF_MODIFIED_SINCE'])){
    $browserModifiedSinceTimestamp = strtotime($_SERVER['HTTP_IF_MODIFIED_SINCE']);
    # The the file's modification time is before or equal to the browser's modification time, this means we do not have a more recent image than the browser, so we can simply return a 304.
    if($fileModificationTimestamp <= $browserModifiedSinceTimestamp){
        http_response_code(304);
        die();
    }
}

# If we reach here, we were not able to skip loading due to caching. Output the modified timestamp so the browser can keep a record of it for the next request.
header("Last-Modified: ".gmdate('D, d M Y H:i:s', $fileModificationTimestamp).' GMT');

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