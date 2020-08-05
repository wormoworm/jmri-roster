<?php
include_once('ui_base.php');
include_once('common/loader.php');
include_once('common/image.php');

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

function outputInfoTableRow($name, $value){
    echo '<tr>
            <td class="tableRowLabel"><p class="label">'.$name.':</p></td>
            <td class="tableRowValue"><p class="value">'.$value.'</p></td>
        </tr>
        ';
}

function outputFunctionTableRow($function){
    echo '<tr>
            <td class="tableRowLabel"><p class="label">'.$function->number.($function->lockable ? '' : ' (momentary)').'</p></td>
            <td class="tableRowValue"><p class="value">'.$function->name.'</p></td>
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

# width="'.$imageDimensions['width'].'" height="'.$imageDimensions['height'].'"
?>

<html>
    <head>
        <link rel="stylesheet" type="text/css" href="<?php if(areURLRewritesAvailable()) echo '../../';?>style.css"/>
        <title><?php echo getPageTitle($locomotive); ?></title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    </head>
    <body>
        <div id="content">
            <div class="contentHorizontalPadding">
                <h1 id="title"><?php echo getPageTitle($locomotive); ?></h1>
                <?php
                # Display the locomotive's name, if it has one.
                if(isSetAndNotEmpty($locomotive->name)){
                    echo '<h2 id="name">'.$locomotive->name.'</h2>
                ';
                }
                # Display the DCC address.
                echo '<h2 id="address" class="valueWithlabel"><span class="valueLabel">Address: </span>'.$locomotive->dccAddress.'</h2>            
            </div>
            ';
            # Display the locomotive's image if available.
            if($locomotive->hasImage()){
                $imageDimensions = getImageDimensions(ROSTER_BASE_PATH.'/'.$locomotive->imageFilePath, $imageWidth);
                $imagePath = areURLRewritesAvailable() ? '../api/v1/locomotive/'.$locomotive->id.'/image/'.$imageWidth : '/api/v1/api_locomotive_image.php?locomotive_id='.$locomotive->id.'&width='.$imageWidth;
                echo '<img id="image" src="'.$imagePath.'"/>
            ';
            }
            ?>
            <div class="contentBlock contentHorizontalPadding contentVerticalPadding">
                <h3 id="locomotiveInfoTitle">Locomotive information</h3>
                <table id="basicInfo" class="valueTable" cellspacing="0" cellpadding="0">
                    <?php
                    outputInfoTableRow('Roster ID', $locomotive->id);
                    if(isSetAndNotEmpty($locomotive->manufacturer)) outputInfoTableRow('Manufacturer', $locomotive->manufacturer);
                    if(isSetAndNotEmpty($locomotive->model)) outputInfoTableRow('Model', $locomotive->model);
                    if(isSetAndNotEmpty($locomotive->owner)) outputInfoTableRow('Owner', $locomotive->owner);
                    if(isSetAndNotEmpty($locomotive->operatingDuration)) outputInfoTableRow('Operating duration', getFriendlyDuration($locomotive->operatingDuration));
                    if(isSetAndNotEmpty($locomotive->lastOperated)) outputInfoTableRow('Last Operated', getFriendlyDate($locomotive->lastOperated).' at '.getFriendlyTime($locomotive->lastOperated));
                    ?>
                </table>
            </div>
                    <?php
                    # The user comment, if set.
                    if(isset($locomotive->comment)){
                        echo '
                        <div class="contentBlock contentHorizontalPadding contentVerticalPadding">
                            <h3 id="commentsTitle">Comment</h3>';
                            $newlineFormattedComment = str_replace(PHP_EOL, '<br/>', $locomotive->comment);
                            echo '<p id="comment" class="body">'.$newlineFormattedComment.'</p>
                        </div>
                        ';
                    }
                    if($locomotive->hasFunctions()){
                        # The function labels, if any are set.
                        echo '
                        <div class="contentBlock contentHorizontalPadding contentVerticalPadding">
                            <h3 id="functionsTitle">Functions</h3>
                                <table id="functions" class="valueTable" cellspacing="0" cellpadding="0">
                                    <tr>
                                        <th>Number</th>
                                        <th>Function</th>
                                    </tr>
                            ';
                            foreach($locomotive->functions as $function){
                                outputFunctionTableRow($function);
                            }
                            echo '</table>
                        </div>
                        ';
                    }
                    ?>
                </div>
            </div>
        </div>
    </body>
</html>