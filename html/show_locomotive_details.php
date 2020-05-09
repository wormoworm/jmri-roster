<?php
include_once('ui_base.php');
include_once('common/loader.php');
include_once('common/image.php');

$rewritesAvailable = true;
if($GLOBALS['DEVELOPMENT_SERVER']) $rewritesAvailable = false;

$imageWidth = 900;

if(!isset($_GET['locomotive_id'])){
    http_response_code(422);
    echo 'Error: locomotive_id not provided';
    die();
}


function getPageTitle($locomotive){
    if(isSetAndNotEmpty($locomotive->number)) return $locomotive->number;
    else return $locomotive->id.' [id]';
}

function outputTableRow($name, $value){
    echo '<tr>
            <td class="tableRowLabel">'.$name.'</td>
            <td class="tableRowValue">'.$value.'</td>
        </tr>
        ';
}



$loader = new Loader(ROSTER_BASE_PATH);
$locomotive = $loader -> loadLocomotive($_GET['locomotive_id']);
if($locomotive==null){
    http_response_code(404);
    echo 'Error: Locomotive with ID '.$_GET['locomotive_id'].' not found';
    die();
}
?>

<html>
    <head>
        <title><?php echo getPageTitle($locomotive); ?></title>
    </head>
    <body>
        <h1 id="number"><?php echo getPageTitle($locomotive); ?></h1>
        <?php
        # Display the locomotive's name, if it has one.
        if(isSetAndNotEmpty($locomotive->name)){
            echo '<h2 id="name">'.$locomotive->name.'</h2>
        ';
        }
        # Display the DCC address.
        echo '<p id="address" class="valueWithlabel"><span class="valueLabel">Address: </span>'.$locomotive->dccAddress.'</p>
        ';
        # Display the locomotive's image if available.
        if(isset($locomotive->imageFilePath)){
            $imageDimensions = getImageDimensions(ROSTER_BASE_PATH.'/'.$locomotive->imageFilePath, $imageWidth);
            $imagePath = $rewritesAvailable ? '../api/v1/locomotive/'.$locomotive->id.'/image/'.$imageWidth : '/api/v1/api_locomotive_image.php?locomotive_id='.$locomotive->id.'&width='.$imageWidth;
            echo '<img id="image" width="'.$imageDimensions['width'].'" height="'.$imageDimensions['height'].'" src="'.$imagePath.'"/>
        ';
        }
        ?>
        <table>
            <?php
            outputTableRow('Roster ID', $locomotive->id);
            if(isSetAndNotEmpty($locomotive->manufacturer)) outputTableRow('Manufacturer', $locomotive->manufacturer);
            if(isSetAndNotEmpty($locomotive->model)) outputTableRow('Model', $locomotive->model);
            if(isSetAndNotEmpty($locomotive->owner)) outputTableRow('Owner', $locomotive->owner);
            if(isSetAndNotEmpty($locomotive->operatingDuration)) outputTableRow('Operating duration', getFriendlyDuration($locomotive->operatingDuration));
            if(isSetAndNotEmpty($locomotive->lastOperated)) outputTableRow('Last Operated', $locomotive->lastOperated);
            ?>
        </table>
        <?php
        # The user comment, if set.
        if(isset($locomotive->comment)){
            $newlineFormattedComment = str_replace(PHP_EOL, '<br/>', $locomotive->comment);
        } echo '<p id="comment" class="body">'.$newlineFormattedComment.'</p>
        ';
        ?>
    </body>
</html>