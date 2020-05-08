<?php
include_once('locomotive.php');
include_once('roster.php');
include_once('utils.php');

class Loader{

    private $rosterBasePath;

    function __construct(string $rosterBasePath){
        $this->rosterBasePath = $rosterBasePath;
    }

    function loadRoster(){
        $startTime = getCurrentTimeMs();
        
        $rosterFile = $this->rosterBasePath . "roster.xml";
        $xml = simplexml_load_file($rosterFile);
        $rosterXML = $xml->children()[0];
    
        $roster = new Roster();
    
        foreach($rosterXML as $locomotiveXML){
            $locomotive = processLocomotiveFromXML($locomotiveXML);
            $roster->addLocomotive($locomotive);
        }
    
        $loadTime = getCurrentTimeMs() - $startTime;
        header('API-Content-Load-Time: ' . $loadTime . 'ms');

        $roster->created = filectime($rosterFile);
        $roster->modified = filemtime($rosterFile);
        $roster->loadTime = $loadTime;

        return $roster;
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