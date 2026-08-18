# Scenario 2: Network Port Scan - Internal Threat Detection

## 📌 Overview

This scenario simulates a **network reconnaissance attack (port scanning)** originating from within the internal network. The attack is detected by Snort IDS running on pfSense, triggering the SOAR pipeline to create a Jira ticket and notify the SOC team via Slack. **No automatic blocking** is applied to prevent self-inflicted disruption of legitimate internal services.

**Threat Type:** Internal (Private IP)  
**Detection Method:** Snort IDS + Zabbix Agent (Log Monitoring)  
**Response:** Passive (Manual investigation required)  
**Response Time:** ~5 seconds  

---

## 🎯 Attack Details

| Attribute | Value |
|-----------|-------|
| **Attack Tool** | Nmap |
| **Attack Vector** | TCP Port Scanning (Reconnaissance) |
| **MITRE Technique** | T1046 - Network Service Discovery |
| **Attacker IP** | `192.168.194.190` (Kali Linux) |
| **Target IP** | `192.168.194.189 (WAN)` (pfSense Firewall) |
| **Target Hostname** | `pfSense-FW` |
| **Scan Type** | SYN Stealth Scan (-sS) |
| **Attack Command** | `nmap -sS -Pn -A -T4 -p 1-2000 192.168.194.189` |

---

## 🔧 Zabbix Configuration

### Snort Integration on pfSense

Snort is installed and configured on pfSense with:

- **Interface Monitoring:** CLIENTS (VLAN 20) for internal traffic inspection
- **Portscan Detection:** Enabled on `vtnet1.20` interface
- **Sensitivity:** Medium (balanced for enterprise environment)
- **Alert Logs:** Stored in `/var/log/snort/snort_vtnet1.20*/alert`

<img width="943" height="282" alt="Snort Interfaces - Active Monitoring" src="https://github.com/user-attachments/assets/d7575bd1-11bb-42e5-a90d-1ac3843efccf" />

### Low-Level Discovery (LLD) for Snort Logs

<img width="1272" height="832" alt="Zabbix LLD - Snort Log Directory Discovery" src="https://github.com/user-attachments/assets/0a524432-2c55-4ae4-8e9c-74592f1f119c" />


**Discovery Configuration:**
- **Rule Name:** Snort Logs Directories
- **Type:** Zabbix Agent (Active)
- **Key:** `snort.interfaces.discovery`
- **Update Interval:** 1 minute
- **Purpose:** Automatically detect new Snort interfaces

### Item: Scan Detection

<img width="844" height="441" alt="Zabbix Item - Snort Scan Log Monitoring" src="https://github.com/user-attachments/assets/0c548104-4520-43a6-89d5-88d4f08fa4f3" />


**Item Configuration:**
- **Type:** Zabbix Agent (Active)
- **Key:** `logrt` with RegEx pattern
- **Purpose:** Detect port scan signatures in Snort logs
- **Update Interval:** 1 second

### RegEx Pre-processing

<img width="840" height="241" alt="Zabbix Preprocessing - Attacker IP Extraction" src="https://github.com/user-attachments/assets/8ee6e1be-7a0a-412f-9ea3-92b7f080b040" />

**RegEx Pattern:** Extracts source IP from Snort scan logs:
```
TCP\s+([\d.]+):\d+\s+->\s+[\d.]+:\d+
```

### Trigger: Network-Port-Scan

<img width="844" height="439" alt="Zabbix Trigger - Network Port Scan" src="https://github.com/user-attachments/assets/ed37e4d0-3df1-47dc-b12e-3b98181bbacd" />


**Trigger Properties:**
- **Name:** Network-Port-Scan
- **Severity:** High
- **Function:** `length() > 0`
- **Condition:** Any detected Nmap scan activity

---

## 💻 Attack Simulation

### Execution from Kali Linux

<img width="519" height="144" alt="Kali Linux - Nmap Port Scan" src="https://github.com/user-attachments/assets/aa9f5f22-9f60-4b35-b385-0c2adc8ffc7e" />

```bash
nmap -sS -Pn -A -T4 -p 1-2000 192.168.194.189
```

**Command Breakdown:**
- `-sS`: SYN stealth scan (half-open)
- `-Pn`: Skip host discovery (assume host is up)
- `-A`: Enable OS and version detection
- `-T4`: Aggressive timing template
- `-p 1-2000`: Scan first 2000 TCP ports
- `192.168.194.189`: Target pfSense firewall

---

## 🔄 SOAR Pipeline Execution

### 1. Alert Generation

<img width="991" height="472" alt="Zabbix Dashboard - Port Scan Alert" src="https://github.com/user-attachments/assets/43d43f6d-06d5-40e9-ba93-ae66673923b8" />


The alert appears in the Problems Dashboard with **High** severity, confirming the Network-Port-Scan detection on host `pfSense-FW`.

### 2. Webhook Transmission

<img width="988" height="428" alt="Zabbix Action Log - Scan Webhook Sent" src="https://github.com/user-attachments/assets/aaeaf30d-bd96-4054-985b-1ff6916f4ca1" />


**Action Log Details:**
- **Status:** Sent ✓
- **Type:** Shuffle Media
- **Attacker IP:** `192.168.194.190`
- **MITRE Technique:** T1046
- **Context:** Network Service Discovery

### 3. Shuffle Workflow Execution

<img width="1176" height="912" alt="Shuffle Workflow - Port Scan Processing" src="https://github.com/user-attachments/assets/b4677043-613a-418a-b27e-51804dc0f7a0" />


**Workflow Path:**
1. Entry Node (Webhook) → Received ✓
2. Python ParseToJSON → Data normalized ✓
3. IP Classification → Detected as Internal ✓
4. Jira 4 - Confirm Private IP → Branch selected ✓
5. Slack 4 → Notification sent ✓

**Key Observation:** The workflow bypasses pfSense blocking nodes since the IP is classified as internal (private network).

### 4. Execution Status

<img width="850" height="235" alt="Shuffle - Execution History" src="https://github.com/user-attachments/assets/06a4534c-0f91-4e10-89ee-5ae051db2431" />


**Execution Metrics:**
- **Status:** FINISHED ✓
- **Processing Time:** Real-time execution
- **All Steps:** Completed successfully

### 5. Raw Payload Reception

<img width="712" height="397" alt="Shuffle - Scan Payload" src="https://github.com/user-attachments/assets/ffbc340b-cacb-4cd1-b251-055aeff44012" />

**Payload Contains:**
- Problem: Network-Port-Scan
- MITRE Technique: T1046
- Complete scan event details
- System metrics
- Attacker context

### 6. Data Normalization

<img width="702" height="522" alt="Shuffle - Parse Output" src="https://github.com/user-attachments/assets/b1ceeb90-8519-4977-9355-e084ab54c88d" />


**Parsed Data:**
```json
{
  "event_id": "1315",
  "problem_name": "Network-Port-Scan",
  "time": "10:51:04",
  "date": "2026.06.19",
  "severity": "High",
  "ioc": "192.168.194.190",
  "host_name": "pfSense-FW",
  "host_id": "10685",
  "host_ip": "192.168.10.100",
  "cpu_usage": "6.7",
  "inbound_traffic": "N/A",
  "outbound_traffic": "N/A",
  "info_url": "https://attack.mitre.org/techniques/T1046/"
}
```

---

## 📋 Jira Ticket Creation

### API Response

<img width="492" height="308" alt="Jira API - Scan Ticket Created" src="https://github.com/user-attachments/assets/0bc157b1-0cad-4f2a-9d43-439d046c95fc" />

**Response Details:**
- **Status:** 201 Created

### Jira Ticket View

<img width="507" height="330" alt="Jira Ticket - Port Scan Internal Threat" src="https://github.com/user-attachments/assets/f087a1dc-405f-4147-9d3d-cdd0af3cf49a" />


**Ticket Details:**
- **Title:** [INTERNAL THREAT] Network-Port-Scan
- **Priority:** High
- **Description includes:**
  - Event ID and timestamp
  - Complete MITRE context (T1046)
  - System metrics
  - Attack details
  - Recommended containment actions

---

## 💬 Slack Notification

### API Response

<img width="515" height="191" alt="Slack API - Scan Notification Delivered" src="https://github.com/user-attachments/assets/00de7cd8-56c7-4152-9117-d7bc14554daf" />

### Slack Alert Card

<img width="424" height="271" alt="Slack - Port Scan Notification Card" src="https://github.com/user-attachments/assets/8b28c31c-41fa-4427-81f2-a87696f01955" />

**Notification Content:**
- **Title:** Zabbix Alert - Intern Threat
- **IP:** `192.168.194.190` (Internal Network)
- **Host:** `pfSense-FW` (`192.168.10.100`)
- **Alert:** Network-Port-Scan at 10:51:04
- **MITRE Link:** Direct URL to T1046
- **Jira Ticket:** with direct link
- **Action Required:** Manual investigation

---

## 📊 Summary

| Step | Component | Status | Output |
|------|-----------|--------|--------|
| 1. Detection | Snort IDS on pfSense | ✅ Success | Port scan detected |
| 2. Log Aggregation | Zabbix Agent | ✅ Success | Snort alerts captured |
| 3. Ingestion | Webhook (Zabbix → Shuffle) | ✅ Success | Payload sent |
| 4. Normalization | Python ParseToJSON | ✅ Success | JSON structured |
| 5. Classification | IP Type Detection | ✅ Success | Identified as Internal |
| 6. Ticketing | Jira API | ✅ Success | Ticket created |
| 7. Notification | Slack API | ✅ Success | Alert sent to SOC team |
| 8. Blocking | pfSense | ⛔ Skipped | No blocking (internal scan) |

---

## 🛡️ Snort Configuration Details

### Portscan Detection Settings

<img width="1325" height="574" alt="Snort - Portscan Detection Configuration" src="https://github.com/user-attachments/assets/16e34f40-cdca-4bec-998d-1f21558790e0" />

**Configuration:**
- **Protocols:** TCP, UDP, ICMP, IP
- **Scan Types:** All (one-to-one, range, distributed)
- **Sensitivity:** Medium
- **Alert Level:** Scan events trigger alerts

### Emerging Threats Rules

<img width="1388" height="742" alt="Snort - Emerging Threats Rules" src="https://github.com/user-attachments/assets/12478022-dc6c-4006-8169-748dc0cb3b6b" />


**Active Rule Categories:**
- `emerging-scan.rules`: Offensive tool signatures
- `emerging-attack_response.rules`: Exploitation patterns
- `emerging-dos.rules`: Denial of service patterns

---

## 📊 Snort Log Structure

### Log Directories

<img width="933" height="166" alt="Snort - Log Directory Structure" src="https://github.com/user-attachments/assets/481f6a5d-1024-4304-aaef-005efaad5c06" />


**Directory Structure:**
```
/var/log/snort/
├── snort_vtnet050537/     # WAN interface alerts
├── snort_vtnet1.2044542/  # CLIENTS interface alerts
│   └── alert              # Raw alert file
└── snort_vtnet2.0xxxxx/   # Other interfaces
```

---

## 🎯 Key Takeaways

1. **Multi-Layer Detection:** The combination of Snort IDS and Zabbix provides comprehensive visibility into reconnaissance activities.

2. **Context-Aware Response:** The SOAR correctly identified the IP as internal and avoided automatic blocking that could disrupt legitimate internal scanning activities.

3. **MITRE ATT&CK Integration:** The alert includes direct links to T1046 (Network Service Discovery) for faster threat understanding.

4. **Automated Discovery:** Zabbix's Low-Level Discovery automatically detects new Snort interfaces without manual configuration.

5. **Operational Intelligence:** The system provides SOC analysts with complete context for investigation while handling repetitive tasks.

---

## 🔗 Related Resources

- [MITRE ATT&CK T1046 - Network Service Discovery](https://attack.mitre.org/techniques/T1046/)
- [Nmap Network Scanning Guide](https://nmap.org/book/)
- [Snort IDS Documentation](https://www.snort.org/documents)
- [pfSense Snort Package Configuration](https://docs.netgate.com/pfsense/en/latest/packages/snort.html)

---

*This scenario demonstrates the SOAR pipeline's effectiveness in detecting and documenting internal reconnaissance activities, providing SOC analysts with comprehensive threat intelligence while avoiding unnecessary automated blocking.*
