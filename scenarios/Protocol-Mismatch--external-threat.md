# Scenario 3: External Protocol Anomaly - Perimeter Threat Response

## 📌 Overview

This scenario simulates a **protocol anomaly attack (Protocol Mismatch)** originating from the external internet. The attack is detected by Snort IDS monitoring the WAN interface, triggering the full automated SOAR pipeline including **threat intelligence enrichment, automatic firewall blocking, ticket lifecycle management, and alert closure** — all without human intervention.

**Threat Type:** External (Public IP)  
**Detection Method:** Snort IDS on WAN Interface + Zabbix Agent  
**Response:** Active (Automatic blocking on pfSense)  
**Response Time:** < 5 seconds  
**MTTR Reduction:** ~93% (from 15 minutes to seconds)

---

## 🎯 Attack Details

| Attribute | Value |
|-----------|-------|
| **Attack Type** | Protocol Mismatch / Anomaly |
| **MITRE Technique** | T1571 - Non-Standard Port / Protocol |
| **Attacker IP** | `185.220.101.5` (External) |
| **Attacker Location** | Germany (DE) |
| **ASN** | 60729 |
| **AS Owner** | Stiftung Erneuerbare Freiheit |
| **Target** | pfSense-FW (WAN Interface) |
| **Attack Pattern** | Malformed packets / Protocol violation |

---

## 🔧 Zabbix Configuration

### Item: Snort Anomalous Connection Logs

![Zabbix Item - Protocol Anomaly Monitoring](https://github.com/user-attachments/assets/a18cfa50-f1d2-434b-84cc-d9b5348c26a5)  
*Figure 7.28 – Zabbix item configuration for monitoring Snort protocol anomalies*

**Item Configuration:**
- **Type:** Zabbix Agent (Active)
- **Key:** `logrt` with RegEx pattern
- **Purpose:** Detect protocol mismatch signatures in Snort WAN logs
- **Update Interval:** 1 second
- **Filter Pattern:** "Protocol mismatch"

### RegEx Pre-processing for External IP Extraction

![Zabbix Preprocessing - External IP Extraction](https://github.com/user-attachments/assets/2c9a5f3e-7627-4244-99af-ffdc75fa27b1)  
*Figure 7.29 – Regular expression preprocessing for external IP extraction*

**RegEx Pattern:** Extracts external IP from Snort WAN logs:
```
TCP\s+([\d.]+):\d+\s+->\s+[\d.]+:\d+
```

### Trigger: Protocol-Mismatch

![Zabbix Trigger - Protocol Mismatch](https://github.com/user-attachments/assets/9f3c0c63-e1a7-4b1d-b4ae-2b7665e31826)  
*Figure 7.30 – Logical expression configuration of the protocol anomaly trigger*

**Trigger Properties:**
- **Name:** Protocol-Mismatch
- **Severity:** High
- **Function:** `length() > 0`
- **Condition:** Any protocol anomaly detected on WAN

---

## 🔄 SOAR Pipeline Execution

### 1. Alert Generation

![Zabbix Dashboard - Protocol Anomaly Alert](https://github.com/user-attachments/assets/63f4e1e0-14e5-4569-81c5-fee5e76e39a5)  
*Figure 7.31 – WAN protocol anomaly alert displayed on Zabbix console*

The alert appears in the Problems Dashboard with **High** severity, confirming the Protocol-Mismatch detection on host `pfSense-FW`.

### 2. Webhook Transmission

![Zabbix Action Log - External Webhook](https://github.com/user-attachments/assets/d5c166bb-8b4f-4ba1-8a55-226b84a78840)  
*Figure 7.32 – Zabbix action log confirming webhook transmission with external IP*

**Action Log Details:**
- **Status:** Sent ✓
- **Type:** Shuffle Media
- **Attacker IP:** `185.220.101.5`
- **MITRE Technique:** T1571

### 3. Shuffle Workflow Execution

![Shuffle Workflow - External Threat Processing](https://github.com/user-attachments/assets/529cb63e-a0c5-4ccc-b9f6-86811c1029a1)  
*Figure 7.33 – Shuffle workflow execution during external incident*

**Workflow Path:**
1. Entry Node (Webhook) → Received ✓
2. Python ParseToJSON → Data normalized ✓
3. IP Classification → Detected as External ✓
4. VirusTotal Enrichment → Malicious confirmed ✓
5. pfSense - Block IP → IP added to alias ✓
6. pfSense - Apply Action → Firewall updated ✓
7. Jira External → Ticket created and completed ✓
8. Zabbix - Close Alert → Alert resolved ✓
9. Slack External → Notification sent ✓

### 4. Execution Status

![Shuffle - External Workflow Status](https://github.com/user-attachments/assets/25f079f1-5f3b-49b5-987d-603c5900e539)  
*Figure 7.34 – Completed external workflow execution status in Shuffle history*

**Execution Metrics:**
- **Status:** FINISHED ✓
- **All Steps:** Completed successfully
- **Processing Time:** < 5 seconds

### 5. Raw Payload Reception

![Shuffle - External Payload](https://github.com/user-attachments/assets/2e0195df-2f48-45b5-9752-999fd261292c)  
*Figure 7.35 – JSON payload of the external incident received on Shuffle webhook*

**Payload Contains:**
- Problem: Protocol-Mismatch
- MITRE Technique: T1571
- Complete alert context
- External IP: 185.220.101.5
- System metrics

### 6. Data Normalization

![Shuffle - Parse Output External](https://github.com/user-attachments/assets/7ae4d90f-1201-4f83-aa32-8f1b1cddff61)  
*Figure 7.36 – Variables extracted and normalized by the Python ParseToJSON node*

**Parsed Data:**
```json
{
  "event_id": "1316",
  "problem_name": "Protocol-Mismatch",
  "time": "11:07:13",
  "date": "2026.06.19",
  "severity": "High",
  "ioc": "185.220.101.5",
  "host_name": "pfSense-FW",
  "host_id": "10685",
  "host_ip": "192.168.10.100",
  "cpu_usage": "6.7",
  "inbound_traffic": "N/A",
  "outbound_traffic": "N/A",
  "info_url": "https://attack.mitre.org/techniques/T1571/"
}
```

---

## 🔍 Threat Intelligence Enrichment

### VirusTotal API Response

![VirusTotal - Malicious IP Confirmation](https://github.com/user-attachments/assets/dc28e55f-9f71-4b22-89a8-78a5dc6a07c0)  
*Figure 7.37 – VirusTotal API response validating malicious score and negative reputation*

**VirusTotal Results:**
```
{
  "reputation": -16,
  "country": "DE",
  "asn": 60729,
  "as_owner": "Stiftung Erneuerbare Freiheit",
  "network_range": "185.220.101.0/24",
  "last_analysis_stats": {
    "malicious": 10,
    "suspicious": 0,
    "harmless": 0,
    "undetected": 0
  }
}
```

**Analysis:** The IP has **10 malicious detections** and a **negative reputation score of -16**, confirming the threat as malicious and triggering automatic remediation.

---

## 📋 Jira Ticket Creation

### API Response

![Jira API - External Ticket Created](https://github.com/user-attachments/assets/cb97bb00-0439-4297-a0d1-115e38090e28)  
*Figure 7.38 – Jira node execution confirming ticket creation*

**Response Details:**
- **Status:** 201 Created
- **Ticket Key:** SOC-99

### Jira Ticket View

![Jira Ticket - External Threat](https://github.com/user-attachments/assets/8204ddf5-c26a-4610-a79e-9ba7a771b33c)  
*Figure 7.39 – Jira ticket containing complete alert details with threat intelligence*

**Ticket Details:**
- **Title:** [EXTERNAL THREAT] Protocol-Mismatch
- **Priority:** High
- **Description includes:**
  - Complete VirusTotal Threat Intelligence
  - Reputation Score: -16
  - Country: Germany (DE)
  - ASN & AS Owner details
  - Network range information
  - 10 malicious detections
  - VT Link for further investigation
  - System metrics at alert time
  - Recommended actions (already executed)

---

## 🛡️ Active Remediation on pfSense

### API Response - Block IP

![pfSense API - IP Added to Blacklist](https://github.com/user-attachments/assets/f242b506-78fb-4a30-a3b4-e1ccc01f34b3)  
*Figure 7.40 – pfSense node execution confirming IP addition to blacklist*

**Response Details:**
- **Status:** 200 OK
- **Action:** IP added to `Shuffle_Blocked_IP` alias
- **IP:** 185.220.101.5

### API Response - Apply Changes

![pfSense API - Changes Applied](https://github.com/user-attachments/assets/aa5cfa92-38ab-437f-928b-7767128ec6b9)  
*Figure 7.41 – pfSense node execution confirming application of changes*

**Response Details:**
- **Status:** 200 OK
- **Action:** Firewall configuration applied
- **Result:** Rules reloaded with new blocking rule

### pfSense Interface Verification

![pfSense - IP Blocked Confirmation](https://github.com/user-attachments/assets/063ae71a-4564-491c-8e50-d00a0f2b20b0)  
*Figure 7.42 – pfSense interface view confirming IP banishment within the blocking alias*

**Alias Details:**
- **Name:** Shuffle_Blocked_IP
- **IP Added:** 185.220.101.5
- **Description:** "Malicious Public IP blocked by Shuffle"
- **Status:** Active

---

## 📝 Jira Ticket Lifecycle Management

### Comment Injection

![Jira API - Comment Added](https://github.com/user-attachments/assets/c3db2cb6-afda-466b-89ba-bee529ac8f20)  
*Figure 7.43 – Jira API response confirming automatic technical comment injection*

### Jira Comment View

![Jira - Technical Comment](https://github.com/user-attachments/assets/ffd4af68-7915-4058-b326-1bd4a50fdeac)  
*Figure 7.44 – Comment added to the Jira ticket*

**Comment Content:**
- Confirmation of automatic blocking
- Firewall action details
- Timestamp of remediation

### Transition to Completed Status

![Jira API - Status Transition](https://github.com/user-attachments/assets/175ad45c-0750-4d6b-8158-2786f966c5e7)  
*Figure 7.45 – Jira API response validating successful ticket state transition*

### Completed Ticket View

![Jira - Completed Ticket](https://github.com/user-attachments/assets/0f265d79-0279-45db-a5e1-38a8b506cebb)  
*Figure 7.46 – Jira interface showing ticket closure and "Completed" status*

**Ticket Final Status:**
- **Status:** Completed ✓
- **Labels:** ExternalThreat, MaliciousIP, VirusTotal-Confirmed
- **Documentation:** Complete with all actions

---

## 🔄 Zabbix Alert Closure

### API Response - Close Alert

![Zabbix API - Alert Closed](https://github.com/user-attachments/assets/31b36993-4d8b-44fe-8c80-8aa06574c776)  
*Figure 7.47 – Zabbix API response confirming remote alert closure*

**Response Details:**
- **Status:** 200 OK
- **Action:** `event.acknowledge` with action=3
- **Message:** "Alerte cloturee automatiquement par Shuffle SOAR. L'IP malveillante a ete bannie avec succes sur le pare-feu PfSense."

### Zabbix Console - Resolved Status

![Zabbix - Alert Resolved](https://github.com/user-attachments/assets/dae7b821-2ed2-4e9e-9276-01bda0485d9e)  
*Figure 7.48 – Zabbix interface confirming alert status changed to "RESOLVED" by API*

**Status Update:**
- **Previous:** Active (High)
- **Current:** RESOLVED ✓
- **Method:** API call from Shuffle

---

## 💬 Slack Closure Notification

### API Response

![Slack API - Closure Notification Sent](https://github.com/user-attachments/assets/516ba1f7-0bde-464f-817b-0d0d357b7bda)  
*Figure 7.49 – Slack API response validating closure notification delivery*

### Slack Final Alert Card

![Slack - External Threat Closure](https://github.com/user-attachments/assets/2d95bb70-a45a-4647-92a6-f15e239c2b60)  
*Figure 7.50 – Closure notification content received on Slack channel*

**Notification Content:**
- **Title:** Zabbix Alert - External Malicious Threat
- **IP:** `185.220.101.5` (External Network)
- **Host:** `pfSense-FW` (`192.168.10.100`)
- **Alert:** Protocol-Mismatch at 11:07:13
- **MITRE Link:** Direct URL to T1571
- **Jira Ticket:** SOC-99 (Completed)
- **Status:** ✅ Fully mitigated

---

## 📊 Complete Workflow Summary

| Step | Component | Status | Output |
|------|-----------|--------|--------|
| 1. Detection | Snort IDS on WAN | ✅ Success | Protocol anomaly detected |
| 2. Log Aggregation | Zabbix Agent | ✅ Success | Snort alerts captured |
| 3. Ingestion | Webhook (Zabbix → Shuffle) | ✅ Success | Payload sent |
| 4. Normalization | Python ParseToJSON | ✅ Success | JSON structured |
| 5. Classification | IP Type Detection | ✅ Success | Identified as External |
| 6. Enrichment | VirusTotal API | ✅ Success | Malicious score confirmed |
| 7. Remediation | pfSense - Block IP | ✅ Success | IP added to alias |
| 8. Apply Changes | pfSense - Apply Action | ✅ Success | Firewall rules reloaded |
| 9. Ticketing | Jira API | ✅ Success | Ticket SOC-99 created |
| 10. Comment | Jira API | ✅ Success | Technical comment added |
| 11. Transition | Jira API | ✅ Success | Status set to Completed |
| 12. Alert Closure | Zabbix API | ✅ Success | Alert resolved |
| 13. Notification | Slack API | ✅ Success | Closure notification sent |

---

## 📈 Performance Metrics

| Metric | Manual Response | Automated (SOAR) | Improvement |
|--------|-----------------|------------------|-------------|
| Detection Time | ~1 minute | ~1 second | ~98% faster |
| Analysis Time | ~5 minutes | ~1 second | ~99% faster |
| Remediation Time | ~9 minutes | ~2 seconds | ~99% faster |
| Total MTTR | ~15 minutes | **< 5 seconds** | **~93% faster** |

---

## 🎯 Key Takeaways

1. **Full Automation:** The entire pipeline—from detection to remediation to notification—executes without human intervention.

2. **Threat Intelligence Integration:** VirusTotal enrichment confirms malicious activity before any blocking action is taken.

3. **Defense in Depth:** Multiple layers of security work together: Snort → Zabbix → Shuffle → pfSense.

4. **Complete Traceability:** Every action is documented in Jira, with clear audit trails for compliance.

5. **Instant Communication:** SOC team receives immediate notification of threat detection and successful mitigation.

6. **Zero-Day Protection:** Protocol anomaly detection catches attacks that don't match known signatures.

7. **Economic Sovereignty:** Open-source stack (Shuffle + Zabbix + Snort + pfSense) provides enterprise-grade protection at minimal cost.

---

## 🔗 Related Resources

- [MITRE ATT&CK T1571 - Non-Standard Port/Protocol](https://attack.mitre.org/techniques/T1571/)
- [VirusTotal API Documentation](https://developers.virustotal.com/reference/overview)
- [pfSense REST API Guide](https://docs.netgate.com/pfsense/en/latest/api/index.html)
- [Snort Protocol Anomaly Detection](https://www.snort.org/faq/readme-protocol-anomaly-detection)

---

*This scenario demonstrates the full capabilities of the SOAR pipeline, showcasing how the system autonomously detects, enriches, remediates, and documents external threats—reducing MTTR from 15 minutes to under 5 seconds while providing complete audit trails and immediate SOC team notification.*