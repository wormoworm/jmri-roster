<?php
ini_set('display_errors', 1);
include_once('locomotive.php');
include_once('utils.php');

class Loader{

    private $rosterBasePath;

    function __construct(string $rosterBasePath){
        $this->rosterBasePath = $rosterBasePath;
    }

    function loadRoster(){
        $startTime = getCurrentTimeMs();
    
        $xml = simplexml_load_file($this->rosterBasePath . "roster.xml");
        $roster = $xml->children()[0];
    
        $locomotives = [];
    
        foreach($roster as $locomotiveXML){
            $locomotive = processLocomotiveFromXML($locomotiveXML);
            $locomotives[] = $locomotive;
        }
    
        $endTime = getCurrentTimeMs();
        error_log("Loaded " . (sizeof($locomotives)) . " locomotives in " . ($endTime - $startTime) . "ms");
    
        return $locomotives;
    }
    
    function loadLocomotive($locomotiveId){
        $startTime = getCurrentTimeMs();
    
        $xml = simplexml_load_file($this->rosterBasePath . 'roster/' . $locomotiveId . '.xml');
        $locomotiveXML = $xml->children()[0];
    
        $locomotive = processLocomotiveFromXML($locomotiveXML);
    
        $endTime = getCurrentTimeMs();
        error_log("Loaded locomotive details in " . ($endTime - $startTime) . "ms");
    
        return $locomotive;
    }
}
?>