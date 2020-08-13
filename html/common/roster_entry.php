<?php
# Holds data for a single roster entry and some related metadata.
class RosterEntry {

    public $locomotive;
    public $created;
    public $modified;
    public $loadTime;

    function __construct(){
        $this->metadata = [];
    }
}
?>