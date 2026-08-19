# Scenario 3: External Protocol Anomaly - Perimeter Threat Response

## 📌 Overview

This scenario simulates a **protocol anomaly attack (Protocol Mismatch)** originating from the external internet. The attack is detected by Snort IDS monitoring the WAN interface, triggering the full automated SOAR pipeline including **threat intelligence enrichment, automatic firewall blocking, ticket lifecycle management, and alert closure** — all without human intervention.

**Threat Type:** External (Public IP)  
**Detection Method:** Snort IDS on WAN Interface + Zabbix Agent  
**Response:** Active (Automatic blocking on pfSense)  
**Response Time:** < 1 minute  
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

<img width="840" height="442" alt="Zabbix Item - Protocol Anomaly Monitoring" src="https://github.com/user-attachments/assets/45061715-bd2d-45a3-9b31-1fb03d605639" />


**Item Configuration:**
- **Type:** Zabbix Agent (Active)
- **Key:** `logrt` with RegEx pattern
- **Purpose:** Detect protocol mismatch signatures in Snort WAN logs
- **Update Interval:** 1 second
- **Filter Pattern:** "Protocol mismatch"

### RegEx Pre-processing for External IP Extraction

<img width="844" height="247" alt="Zabbix Preprocessing - External IP Extraction" src="https://github.com/user-attachments/assets/12e56774-1fda-4d00-8189-4604a2c0deeb" />


**RegEx Pattern:** Extracts external IP from Snort WAN logs:
```
TCP\s+([\d.]+):\d+\s+->\s+[\d.]+:\d+
```

### Trigger: Protocol-Mismatch

<img width="844" height="438" alt="Zabbix Trigger - Protocol Mismatch" src="https://github.com/user-attachments/assets/1c9792af-d3d5-4d15-855c-7bbec3436d11" />


**Trigger Properties:**
- **Name:** Protocol-Mismatch
- **Severity:** High
- **Function:** `length() > 0`
- **Condition:** Any protocol anomaly detected on WAN

---

## 🔄 SOAR Pipeline Execution

### 1. Alert Generation

<img width="993" height="471" alt="Zabbix Dashboard - Protocol Anomaly Alert" src="https://github.com/user-attachments/assets/aadcca06-d070-4acd-8a64-30872286a906" />


The alert appears in the Problems Dashboard with **High** severity, confirming the Protocol-Mismatch detection on host `pfSense-FW`.

### 2. Webhook Transmission

<img width="986" height="427" alt="Zabbix Action Log - External Webhook" src="https://github.com/user-attachments/assets/5652de18-1c4d-4129-a1e6-ffe8928f042a" />


**Action Log Details:**
- **Status:** Sent ✓
- **Type:** Shuffle Media
- **Attacker IP:** `185.220.101.5`
- **MITRE Technique:** T1571

### 3. Shuffle Workflow Execution

<img width="1321" height="619" alt="Shuffle Workflow - External Threat Processing" src="https://github.com/user-attachments/assets/aa9a0536-f105-4df4-9183-c13139459930" />



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

<img width="817" height="199" alt="Shuffle - External Workflow Status" src="https://github.com/user-attachments/assets/f21e3c0b-cf2b-4b73-85ee-b64a5572e26b" />


**Execution Metrics:**
- **Status:** FINISHED ✓
- **All Steps:** Completed successfully
- **Processing Time:** < 5 seconds

### 5. Raw Payload Reception

<img width="708" height="405" alt="Shuffle - External Payload" src="https://github.com/user-attachments/assets/61d5c8f0-84bb-443a-be92-5cd2c79b9d67" />



**Payload Contains:**
- Problem: Protocol-Mismatch
- MITRE Technique: T1571
- Complete alert context
- External IP: 185.220.101.5
- System metrics

### 6. Data Normalization

<img width="712" height="519" alt="Shuffle - Parse Output External" src="https://github.com/user-attachments/assets/58c60924-a02c-4616-b861-286160f83a92" />


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

<img width="936" height="487" alt="VirusTotal - Malicious IP Confirmation" src="https://github.com/user-attachments/assets/afce6a07-67be-4f03-a0be-e41743baeca7" />


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

<img width="403" height="173" alt="Jira API - External Ticket Created" src="https://github.com/user-attachments/assets/8d2aa222-3c6a-4365-8caf-34c8027958f3" />



**Response Details:**
- **Status:** 201 Created

### Jira Ticket View

<img width="407" height="456" alt="Jira Ticket - External Threat" src="https://github.com/user-attachments/assets/8f9b8d3c-096e-4e62-9b8d-a933c5502883" />



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

<img width="709" height="532" alt="pfSense API - IP Added to Blacklist" src="https://github.com/user-attachments/assets/d8a248ec-31d9-4959-b914-c42618358e9a" />


**Response Details:**
- **Status:** 200 OK
- **Action:** IP added to `Shuffle_Blocked_IP` alias
- **IP:** 185.220.101.5

### API Response - Apply Changes

<img width="706" height="507" alt="pfSense API - Changes Applied" src="https://github.com/user-attachments/assets/b817888d-3655-4dcf-a4aa-a96455d9cec5" />


**Response Details:**
- **Status:** 200 OK
- **Action:** Firewall configuration applied
- **Result:** Rules reloaded with new blocking rule

### pfSense Interface Verification

<img width="976" height="280" alt="pfSense - IP Blocked Confirmation" src="https://github.com/user-attachments/assets/ddc8276d-591f-4b8c-ab2a-de593ba0ab59" />


**Alias Details:**
- **Name:** Shuffle_Blocked_IP
- **IP Added:** 185.220.101.5
- **Description:** "Malicious Public IP blocked by Shuffle"
- **Status:** Active

---

## 📝 Jira Ticket Lifecycle Management

### Comment Injection

<img width="383" height="274" alt="Jira API - Comment Added" src="https://github.com/user-attachments/assets/1d42a8e4-198f-4b0f-b02a-e6805e79a362" />

### Jira Comment View

<img width="1153" height="291" alt="Jira - Technical Comment" src="https://github.com/user-attachments/assets/81dedfc4-9e1f-4abe-b022-eb288590b731" />


**Comment Content:**
- Confirmation of automatic blocking
- Firewall action details
- Timestamp of remediation

### Transition to Completed Status

<img width="418" height="200" alt="Jira API - Status Transition" src="https://github.com/user-attachments/assets/566d56ca-4319-42cc-9c1b-f932d7b85006" />


### Completed Ticket View

<img width="642" height="646" alt="Jira - Completed Ticket" src="https://github.com/user-attachments/assets/7446347c-8faf-4151-a3e1-94a94b5364b2" />


**Ticket Final Status:**
- **Status:** Completed ✓
- **Labels:** ExternalThreat, MaliciousIP, VirusTotal-Confirmed
- **Documentation:** Complete with all actions

---

## 🔄 Zabbix Alert Closure

### API Response - Close Alert

<img width="406" height="251" alt="Zabbix API - Alert Closed" src="https://github.com/user-attachments/assets/be42b807-a656-4014-bb33-82f85621813c" />


**Response Details:**
- **Status:** 200 OK
- **Action:** `event.acknowledge` with action=3
- **Message:** "Alerte cloturee automatiquement par Shuffle SOAR. L'IP malveillante a ete bannie avec succes sur le pare-feu PfSense."

### Zabbix Console - Resolved Status

<img width="985" height="469" alt="Zabbix - Alert Resolved" src="https://github.com/user-attachments/assets/cfc1fe74-70a6-4fc3-9171-8c6ba4261a49" />


**Status Update:**
- **Previous:** Active (High)
- **Current:** RESOLVED ✓
- **Method:** API call from Shuffle

---

## 💬 Slack Closure Notification

### API Response

<img width="379" height="271" alt="Slack API - Closure Notification Sent" src="https://github.com/user-attachments/assets/d540c05c-54b5-42e2-be66-dcce53716c14" />


### Slack Final Alert Card

<img width="422" height="146" alt="Slack - External Threat Closure" src="https://github.com/user-attachments/assets/716c18bc-3a12-4d08-8eb7-d95f62472267" />


**Notification Content:**
- **Title:** Zabbix Alert - External Malicious Threat
- **IP:** `185.220.101.5` (External Network)
- **Host:** `pfSense-FW` (`192.168.10.100`)
- **Alert:** Protocol-Mismatch at 11:07:13
- **MITRE Link:** Direct URL to T1571
- **Jira Ticket:**  (Completed)
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
| 9. Ticketing | Jira API | ✅ Success | Ticket created |
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
| Remediation Time | ~9 minutes | ~30 second | ~99% faster |
| Total MTTR | ~15 minutes | **52 s (< 1 min)** | **~93% faster** |

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

*This scenario demonstrates the full capabilities of the SOAR pipeline, showcasing how the system autonomously detects, enriches, remediates, and documents external threats—reducing MTTR from 15 minutes to under 1 minute while providing complete audit trails and immediate SOC team notification.*
