// Zabbix Webhook media type script — forwards triggered alerts to Shuffle
// Configured under: Alerts > Media types > Shuffle (Webhook type)
// Expects the following parameters (set in the media type's Parameters tab):
//   HTTPProxy -> Content-Type header value (e.g. "application/json")
//   Message   -> {ALERT.MESSAGE}
//   Subject   -> {ALERT.SUBJECT}
//   To        -> {ALERT.SENDTO}
//   URL       -> Shuffle webhook endpoint URL

try {
    // Zabbix passes all configured parameters as a single JSON string in `value`
    var params = JSON.parse(value);

    // Build the outgoing HTTP request to the Shuffle webhook
    var req = new HttpRequest();
    req.addHeader('Content-Type: ' + params.HTTPProxy);

    // Payload forwarded to Shuffle — subject/message default to empty
    // strings if Zabbix didn't populate them for this event
    var payload = {
        subject: params.Subject || '',
        message: params.Message || ''
    };

    // Send the alert to Shuffle's webhook trigger
    var response = req.post(params.URL, JSON.stringify(payload));

    // Log the response for troubleshooting in Zabbix's media type logs
    Zabbix.log(4, '[Shuffle Webhook] Response: ' + response);
    return 'OK';
}
catch (error) {
    // Log and surface any failure (bad URL, network error, malformed JSON, etc.)
    Zabbix.log(4, '[Shuffle Webhook] Error: ' + error);
    return 'Sending failed: ' + error;
}