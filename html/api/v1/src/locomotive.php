<?php

class Locomotive {

    // Required properties - these are passed to the constructor.
    public $id;
    public $dccAddress;
    public $name;
    
    // Optional properties - these can be set after the constructor.
    public $manufacturer;
    public $model;
    public $owner;
    public $comment;
    public $imageFilePath;

    function __construct(string $id, string $dccAddress, string $name){
        $this->id = $id;
        $this->dccAddress = $dccAddress;
        $this->name = $name;
    }
}

function processLocomotiveFromXML($locomotiveXML): Locomotive {
    $attributes = $locomotiveXML->attributes();
    return new Locomotive($attributes['id'], $attributes['dccAddress'], $attributes['fileName']);
}
?>