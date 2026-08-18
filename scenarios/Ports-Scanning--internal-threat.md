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
| **Target IP** | `192.168.194.189` (pfSense Firewall) |
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

![Snort Interfaces - Active Monitoring](https://github.com/user-attachments/assets/8b3b5f0f-2b12-41dc-8beb-2f7e1cf6e49b)  
*Figure 6.14 – Snort activation on WAN and CLIENTS interfaces*

### Low-Level Discovery (LLD) for Snort Logs

![Zabbix LLD - Snort Log Directory Discovery](https://github.com/user-attachments/assets/9c3a0d20-8f9e-4194-b616-ffcc19cafecb)  
*Figure 6.23 – Zabbix rule for discovering Snort log directories*

**Discovery Configuration:**
- **Rule Name:** Snort Logs Directories
- **Type:** Zabbix Agent (Active)
- **Key:** `snort.interfaces.discovery`
- **Update Interval:** 1 minute
- **Purpose:** Automatically detect new Snort interfaces

### Item: Scan Detection

![Zabbix Item - Snort Scan Log Monitoring](https://github.com/user-attachments/assets/cf7ca3fa-7a84-4a55-88eb-3a135ba93f7b)  
*Figure 7.14 – Configuration of the item monitoring Snort port scan events*

**Item Configuration:**
- **Type:** Zabbix Agent (Active)
- **Key:** `logrt` with RegEx pattern
- **Purpose:** Detect port scan signatures in Snort logs
- **Update Interval:** 1 second

### RegEx Pre-processing

![Zabbix Preprocessing - Attacker IP Extraction](https://github.com/user-attachments/assets/2b1aa395-9074-4f05-a506-bb01f31e1763)  
*Figure 7.15 – Regular expression configuration for extracting attacker IP*

**RegEx Pattern:** Extracts source IP from Snort scan logs:
```
TCP\s+([\d.]+):\d+\s+->\s+[\d.]+:\d+
```

### Trigger: Network-Port-Scan

![Zabbix Trigger - Network Port Scan](https://github.com/user-attachments/assets/25c80c04-13a0-4f81-a6e5-82f54e5874fa)  
*Figure 7.16 – Configuration of the port scan trigger*

**Trigger Properties:**
- **Name:** Network-Port-Scan
- **Severity:** High
- **Function:** `length() > 0`
- **Condition:** Any detected Nmap scan activity

---

## 💻 Attack Simulation

### Execution from Kali Linux

![Kali Linux - Nmap Port Scan](https://github.com/user-attachments/assets/674a9993-61c1-49a4-b99f-b9f5d662d6f3)  
*Figure 7.17 – Kali Linux terminal illustrating Nmap reconnaissance scan*

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

![Zabbix Dashboard - Port Scan Alert](https://github.com/user-attachments/assets/856afb67-a78b-4828-aac4-f3ad21893f2b)  
*Figure 7.18 – Port scan alert captured and displayed on Zabbix console*

The alert appears in the Problems Dashboard with **High** severity, confirming the Network-Port-Scan detection on host `pfSense-FW`.

### 2. Webhook Transmission

![Zabbix Action Log - Scan Webhook Sent](https://github.com/user-attachments/assets/68ec123a-b88c-47fe-bb4e-2a34910fbf15)  
*Figure 7.19 – Zabbix action log confirming scan webhook transmission*

**Action Log Details:**
- **Status:** Sent ✓
- **Type:** Shuffle Media
- **Attacker IP:** `192.168.194.190`
- **MITRE Technique:** T1046
- **Context:** Network Service Discovery

### 3. Shuffle Workflow Execution

![Shuffle Workflow - Port Scan Processing](https://github.com/user-attachments/assets/499d6dd2-d97c-4f8f-9703-8bef3faac7fe)  
*Figure 7.20 – Shuffle workflow execution triggered during port scan*

**Workflow Path:**
1. Entry Node (Webhook) → Received ✓
2. Python ParseToJSON → Data normalized ✓
3. IP Classification → Detected as Internal ✓
4. Jira 4 - Confirm Private IP → Branch selected ✓
5. Slack 4 → Notification sent ✓

**Key Observation:** The workflow bypasses pfSense blocking nodes since the IP is classified as internal (private network).

### 4. Execution Status

![Shuffle - Execution History](https://github.com/user-attachments/assets/5619d887-267b-4375-858c-12a9b599c1ba)  
*Figure 7.21 – Completed workflow execution status in Shuffle history*

**Execution Metrics:**
- **Status:** FINISHED ✓
- **Processing Time:** Real-time execution
- **All Steps:** Completed successfully

### 5. Raw Payload Reception

![Shuffle - Scan Payload](https://github.com/user-attachments/assets/d987981c-f89d-4c3e-82f1-d7df9234a60d)  
*Figure 7.22 – JSON payload of the port scan incident received on Shuffle webhook*

**Payload Contains:**
- Problem: Network-Port-Scan
- MITRE Technique: T1046
- Complete scan event details
- System metrics
- Attacker context

### 6. Data Normalization

![Shuffle - Parse Output](https://github.com/user-attachments/assets/c3b43f44-94e8-4d48-91d6-944a39c08751)  
*Figure 7.23 – Information extraction via the data processing node*

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

![Jira API - Scan Ticket Created](https://github.com/user-attachments/assets/00b6f56e-82b6-4ac0-9aa2-c0d28f22a1c8)  
*Figure 7.24 – Jira API response confirming the creation of the scan incident ticket*

**Response Details:**
- **Status:** 201 Created
- **Ticket Key:** `SOC-98`

### Jira Ticket View

![Jira Ticket - Port Scan Internal Threat](https://github.com/user-attachments/assets/8ec277ec-f78c-4870-a3a2-9e8e84c04177)  
*Figure 7.25 – Jira interface showing the generated port scan incident ticket*

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

![Slack API - Scan Notification Delivered](https://github.com/user-attachments/assets/111713ab-6b08-42eb-9156-9eb7a02666f0)  
*Figure 7.26 – Slack API response confirming scan notification delivery*

### Slack Alert Card

![Slack - Port Scan Notification Card](https://github.com/user-attachments/assets/8cb7a47c-b27e-4cf1-95ac-ed51d9fe8d6a)  
*Figure 7.27 – Alert card received in real-time on the SOC Slack channel*

**Notification Content:**
- **Title:** Zabbix Alert - Intern Threat
- **IP:** `192.168.194.190` (Internal Network)
- **Host:** `pfSense-FW` (`192.168.10.100`)
- **Alert:** Network-Port-Scan at 10:51:04
- **MITRE Link:** Direct URL to T1046
- **Jira Ticket:** SOC-98 with direct link
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
| 6. Ticketing | Jira API | ✅ Success | Ticket SOC-98 created |
| 7. Notification | Slack API | ✅ Success | Alert sent to SOC team |
| 8. Blocking | pfSense | ⛔ Skipped | No blocking (internal scan) |

---

## 🛡️ Snort Configuration Details

### Portscan Detection Settings

![Snort - Portscan Detection Configuration](https://github.com/user-attachments/assets/52154bb9-29d8-4d9c-95d7-2dba31fa9256)  
*Figure 6.16 – Activation of port scan detection in Snort*

**Configuration:**
- **Protocols:** TCP, UDP, ICMP, IP
- **Scan Types:** All (one-to-one, range, distributed)
- **Sensitivity:** Medium
- **Alert Level:** Scan events trigger alerts

### Emerging Threats Rules

![Snort - Emerging Threats Rules](https://github.com/user-attachments/assets/c52ebc7b-6a61-450b-8ef6-bc8887a3cd6d)  
*Figure 6.17 – Activation of Emerging Threats rule categories*

**Active Rule Categories:**
- `emerging-scan.rules`: Offensive tool signatures
- `emerging-attack_response.rules`: Exploitation patterns
- `emerging-dos.rules`: Denial of service patterns

---

## 📊 Snort Log Structure

### Log Directories

![Snort - Log Directory Structure](https://github.com/user-attachments/assets/0e14a30d-68e0-4149-9d1f-16fcc07ae1bc)  
*Figure 6.15 – Snort log file directory structure*

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