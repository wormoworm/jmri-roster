<?php

include_once('utils.php');

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
define('KEY_ATTRIBUTE_PAIRS', 'attributepairs');
define('KEY_KEY_VALUE_PAIR', 'keyvaluepair');
define('KEY_KEY', 'key');
define('KEY_VALUE', 'value');

define('ATTRIBUTE_NAME', 'Name');
define('ATTRIBUTE_OPERATING_DURATION', 'OperatingDuration');
define('ATTRIBUTE_LAST_OPERATED', 'LastOperated');

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
    public $operatingDuration;
    public $lastOperated;

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
    setStringPropertyIfAvailable($attributes[KEY_MANUFACTURER], $locomotive->manufacturer);
    setStringPropertyIfAvailable($attributes[KEY_MODEL], $locomotive->model);
    setStringPropertyIfAvailable($attributes[KEY_OWNER], $locomotive->owner);
    setStringPropertyIfAvailable($attributes[KEY_COMMENT], $locomotive->comment);
    if(isSetAndNotEmpty($attributes[KEY_IMAGE_FILE_PATH])){
        $imagePathPieces = explode(FORWARD_SLASH, $attributes[KEY_IMAGE_FILE_PATH]);
        $relativePathPieces = array($imagePathPieces[sizeof($imagePathPieces)-2], $imagePathPieces[sizeof($imagePathPieces)-1]);
        $relativeImagePath = join(FORWARD_SLASH, $relativePathPieces);
        $locomotive->imageFilePath = $relativeImagePath;
    }
    # Check if there are any key-value pairs we might be interested in. These are in <locomotive> => <attributepairs>.
    $attributePairs = $locomotiveXML->xpath(KEY_ATTRIBUTE_PAIRS.'/'.KEY_KEY_VALUE_PAIR);
    // print_r($attributePairs);
    foreach($attributePairs as $attributePair){
        $key = (string) $attributePair->xpath(KEY_KEY)[0];
        $value = (string )$attributePair->xpath(KEY_VALUE)[0];
        switch($key){
            case ATTRIBUTE_NAME:
                $locomotive->name = $value;
                break;
            case ATTRIBUTE_OPERATING_DURATION:
                $locomotive->operatingDuration = $value;
                break;
            case ATTRIBUTE_LAST_OPERATED:
                $locomotive->lastOperated = strtotime($value);
                break;
        }
    }
    return $locomotive;
}

function setStringPropertyIfAvailable($source, &$destination){
    if (isSetAndNotEmpty($source)) $destination = (string) $source;
}
?>