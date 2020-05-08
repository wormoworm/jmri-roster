<?php
# Holds roster locomotive data and some related metadata.
class Roster {

    public $locomotives;
    public $created;
    public $modified;
    public $loadTime;

    function __construct(){
        $this->locomotives = [];
        $this->metadata = [];
    }

    function addLocomotive($locomotive){
        $this->locomotives[] = $locomotive;
    }

    function getLocomotiveCount(){
        return sizeof($this->locomotives);
    }
}
?>