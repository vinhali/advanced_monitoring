<?php

$user         = "glpi";
$password     = "glpi";
$xmlhost      = "127.0.0.1";
$xmlurl       = "glpi/plugins/webservices/xmlrpc.php";
$watcher      = "2";
$watchergroup = "1";
$sqlhost      = "127.0.0.1";
$sqldb        = "glpidb";
$sqluser      = "root";
$sqlpwd       = "root";

// ------------------------------------------------------------------------------------------------------------------------

$arg[]    = "method=glpi.test";
$arg[]    = "url=$xmlurl";
$arg[]    = "host=$xmlhost";
$response = getxml($arg);

unset($arg);
$webservices_version = $response['webservices'];
$eventval            = array();
if ($argv > 1) {
    for ($i = 1; $i < count($argv); $i++) {
        $it               = explode("=", $argv[$i], 2);
        $it[0]            = preg_replace('/^--/', '', $it[0]);
        $eventval[$it[0]] = (isset($it[1]) ? $it[1] : true);
    }
}
$eventhost         = $eventval['eventhost'];
$event             = $eventval['event'];
$state             = $eventval['state'];
$servico           = $eventval['servico'];
$eventansible      = $eventval['eventansible'];
$triggerid         = $eventval['triggerid'];
unset($eventval);

function getxml($arg)
{
    $args = array();
    if ($arg > 1) {
        for ($i = 0; $i < count($arg); $i++) {
            $it    = explode("=", $arg[$i], 2);
            $it[0] = preg_replace('/^--/', '', $it[0]);
            if (strpos($it[1], ',') !== false) {
                $it[1] = explode(",", $it[1]);
            }
            $args[$it[0]] = (isset($it[1]) ? $it[1] : true);
        }
    }
    $method = $args['method'];
    $url    = $args['url'];
    $host   = $args['host'];
    
    if (isset($args['session'])) {
        $url .= '?session=' . $args['session'];
        unset($args['session']);
    }
    $header = "Content-Type: text/xml";
    echo "[INFO] Calling '$method' on http://$host/$url [ok]\n";
    
    $request = xmlrpc_encode_request($method, $args);
    $context = stream_context_create(array(
        'http' => array(
            'method' => "POST",
            'header' => $header,
            'content' => $request
        )
    ));
    $file    = file_get_contents("http://$host/$url", false, $context);
    if (!$file) {
        die("+ No response\n");
    }
    
    
    if (in_array('Content-Encoding: deflate', $http_response_header)) {
        $lenc = strlen($file);
        echo "[INFO] Compressed response : $lenc\n";
        $file = gzuncompress($file);
        $lend = strlen($file);
        echo "[INFO] Uncompressed response : $lend (" . round(100.0 * $lenc / $lend) . "%)\n";
    }
    
    $response = xmlrpc_decode($file);
    if (!is_array($response)) {
        echo $file;
        die("[INFO] Bad response\n");
    }
    if (xmlrpc_is_fault($response)) {
        echo ("[INFO] xmlrpc error(" . $response['faultCode'] . "): " . $response['faultString'] . "\n");
    } else {
        return $response;
    }
}
if (!extension_loaded("xmlrpc")) {
    die("[INFO] Extension xmlrpc not loaded\n");
}


if ($event == "OPEN") {
    $arg[]    = "method=glpi.doLogin";
    $arg[]    = "url=$xmlurl";
    $arg[]    = "host=$xmlhost";
    $arg[]    = "login_password=$password";
    $arg[]    = "login_name=$user";
    $response = getxml($arg);
    $session  = $response['session'];
    unset($arg);
	unset($response);
	
    if (!empty($session)) {
        $title   = "$triggerid: $eventhost - $servico - Analytical Crisis IA [$state]";
        $content = "Nome do host: $eventhost. ID da trigger: $triggerid. Status da trigger: $state.";
		$arg[]      = "method=glpi.listDropdownValues";
		$arg[]      = "url=$xmlurl";
		$arg[]      = "host=$xmlhost";
		$arg[]      = "session=$session";
		$arg[]      = "dropdown=itilcategories";
		$response   = getxml($arg);
		unset($arg);
        if (!empty($watcher)) {
            $watcherarg = "observer=$watcher";
        } elseif (!empty($watchergroup)) {
            $arg[]    = "method=glpi.listUsers";
            $arg[]    = "url=$xmlurl";
            $arg[]    = "host=$xmlhost";
            $arg[]    = "session=$session";
            $arg[]    = "group=$watchergroup";
            $response = getxml($arg);
            foreach ($response as $user) {
                $watcherids .= $user['id'] . ",";
            }
            $watcherids = rtrim($watcherids, ",");
            $watcherarg = "observer=$watcherids";
            unset($arg);
        } else {
            // uso futuro
        }
        
        $arg[] = "method=glpi.createTicket";
        $arg[] = "url=$xmlurl";
        $arg[] = "host=$xmlhost";
        $arg[] = "session=$session";
        $arg[] = "title=$title";
        $arg[] = "content=$content";
        $arg[] = "urgancy=5";
        if (!empty($catarg))
            $arg[] = $catarg;
        if (!empty($watcherarg))
            $arg[] = $watcherarg;
        if (str_replace(".", "", $webservices_version) >= '120') {
            $arg[] = "use_email_notification=1";
        }
        $response = getxml($arg);
        unset($arg);
        unset($response);
        
        $arg[] = "method=glpi.doLogout";
        $arg[] = "url=$xmlurl";
        $arg[] = "host=$xmlhost";
        $arg[] = "session=$session";
        
        $response = getxml($arg);
        unset($arg);
        unset($response);

    }
}

?>
