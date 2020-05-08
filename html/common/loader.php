<?php
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
    
        $loadTime = getCurrentTimeMs() - $startTime;
        header('API-Content-Load-Time: ' . $loadTime . 'ms');

        return $locomotives;
    }
    
    function loadLocomotive($locomotiveId){
        $startTime = getCurrentTimeMs();

        $locomotiveFile = $this->rosterBasePath . 'roster/' . $locomotiveId . '.xml';

        if(file_exists($locomotiveFile)){    
            $xml = simplexml_load_file($locomotiveFile);
            $locomotiveXML = $xml->children()[0];
        
            $locomotive = processLocomotiveFromXML($locomotiveXML);
        
            $loadTime = getCurrentTimeMs() - $startTime;
            header('API-Content-Load-Time: ' . $loadTime . 'ms');
        
            return $locomotive;
        }
        else{
            return null;
        }
    }
}
?>