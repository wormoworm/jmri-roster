<?php

define('KEY_ID', 'id');
define('KEY_DCC_ADDRESS', 'dccAddress');
define('KEY_FILE_NAME', 'fileName');
define('KEY_NUMBER', 'roadNumber');
define('KEY_NAME', 'roadName');
define('KEY_MANUFACTURER', 'mfg');
define('KEY_MODEL', 'model');
define('KEY_OWNER', 'owner');
define('KEY_COMMENT', 'comment');
define('KEY_IMAGE_FILE_PATH', 'imageFilePath');

define('FORWARD_SLASH', '/');

class Locomotive {

    // Required properties - these are passed to the constructor.
    public $id;
    public $dccAddress;
    public $fileName;
    
    // Optional properties - these can be set after the constructor.
    public $number;
    public $name;
    public $manufacturer;
    public $model;
    public $owner;
    public $comment;
    public $imageFilePath;

    function __construct(string $id, string $dccAddress, string $fileName){
        $this->id = $id;
        $this->dccAddress = $dccAddress;
        $this->fileName = $fileName;
    }
}

function processLocomotiveFromXML($locomotiveXML): Locomotive {
    $attributes = $locomotiveXML->attributes();
    // Create the Locomotive object with the required fields.
    $locomotive = new Locomotive($attributes[KEY_ID], $attributes[KEY_DCC_ADDRESS], $attributes[KEY_FILE_NAME]);
    // Add each of the optional fields, if available.
    setStringPropertyIfAvailable($attributes[KEY_NUMBER], $locomotive->number);
    setStringPropertyIfAvailable($attributes[KEY_NAME], $locomotive->name);
    setStringPropertyIfAvailable($attributes[KEY_MANUFACTURER], $locomotive->manufacturer);
    setStringPropertyIfAvailable($attributes[KEY_MODEL], $locomotive->model);
    setStringPropertyIfAvailable($attributes[KEY_OWNER], $locomotive->owner);
    setStringPropertyIfAvailable($attributes[KEY_COMMENT], $locomotive->comment);
    if(isSetAndNotEmpty($attributes[KEY_IMAGE_FILE_PATH])){
        $imagePathPieces = explode(FORWARD_SLASH, $attributes[KEY_IMAGE_FILE_PATH]);
        $relativePathPieces = array('jmri-data', $imagePathPieces[sizeof($imagePathPieces)-2], $imagePathPieces[sizeof($imagePathPieces)-1]);
        $relativeImagePath = join(FORWARD_SLASH, $relativePathPieces);
        $locomotive->imageFilePath = $relativeImagePath;
    }
    return $locomotive;
}

function isSetAndNotEmpty($value){
    return isset($value) && $value != "";
}

function setStringPropertyIfAvailable($source, &$destination){
    if (isSetAndNotEmpty($source)) $destination = (string) $source;
}
?>