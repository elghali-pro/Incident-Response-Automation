#!/usr/local/bin/php
<?php
/**
 * Snort Log Directory Discovery Script for Zabbix LLD
 * 
 * This script automatically discovers Snort log directories on pfSense
 * and returns them in a JSON format compatible with Zabbix Low-Level Discovery (LLD).
 * 
 * Purpose:
 * - Dynamically detect all Snort interface log directories
 * - Eliminate manual configuration for new Snort interfaces
 * - Enable automatic creation of Zabbix items and triggers for new Snort instances
 * 
 * Usage:
 * - Called by Zabbix Agent via UserParameter in pfSense
 * - Returns JSON array for Zabbix LLD processing
 * 
 * Example Output:
 * [
 *   {"#SNORTDIR": "snort_vtnet050537"},
 *   {"#SNORTDIR": "snort_vtnet1.2044542"}
 * ]
 * 
 */

// Discover all Snort log directories in /var/log/snort/
// The glob pattern matches any directory starting with "snort_"
$dirs = glob("/var/log/snort/snort_*", GLOB_ONLYDIR);

// Initialize an empty array to store the discovered directories
$json = [];

// Iterate through each discovered directory
foreach($dirs as $d) {
    // Extract only the directory name (not the full path)
    // Example: "/var/log/snort/snort_vtnet050537" -> "snort_vtnet050537"
    $dirName = basename($d);
    
    // Build the JSON structure required by Zabbix LLD
    // The macro "#SNORTDIR" will be used by Zabbix to create items
    $json[] = ["#SNORTDIR" => $dirName];
}

// Output the JSON encoded array
// This format is consumed by Zabbix Low-Level Discovery rules
echo json_encode($json);

// Exit with success status
exit(0);
?>