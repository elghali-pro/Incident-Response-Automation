# Scenario 1: SSH Bruteforce - Internal Threat Detection

## 📌 Overview

This scenario simulates a **dictionary-based SSH bruteforce attack** originating from within the internal network. The attack is detected by Zabbix monitoring the authentication logs, triggering the SOAR pipeline to create a Jira ticket and notify the SOC team via Slack. **No automatic blocking** is applied to prevent self-inflicted DoS on internal infrastructure.

**Threat Type:** Internal (Private IP)  
**Detection Method:** Zabbix Agent monitoring `/var/log/auth.log`  
**Response:** Passive (Manual investigation required)  
**Response Time:** ~6 seconds  

---

## 🎯 Attack Details

| Attribute | Value |
|-----------|-------|
| **Attack Tool** | Hydra |
| **Attack Vector** | SSH Service (Port 22) |
| **Attacker IP** | `192.168.20.152` (Kali Linux) |
| **Target IP** | `192.168.20.151` (Ubuntu Server) |
| **Target Hostname** | `ubuntu-client1` |
| **Dictionary** | `rockyou.txt` |
| **Threshold** | >5 failed attempts in 10 seconds |
| **Attack Command** | `hydra -l client1 -P /usr/share/wordlists/rockyou.txt -t 4 ssh://192.168.20.151` |

---

## 🔧 Zabbix Configuration

### Item: Capture malicious IP from /var/log/auth.log
 
<img width="1111" height="595" alt="Zabbix Item Configuration - Auth Log Monitoring" src="https://github.com/user-attachments/assets/d01bc01e-645c-4771-b68f-a3b12bfb7710" />

**Item Configuration:**
- **Type:** Zabbix Agent (Active)
- **Key:** `logrt` with RegEx pattern
- **Purpose:** Extract attacker IP from authentication logs
- **Update Interval:** 1 second

### Trigger: SSH-Bruteforce Detected

<img width="1201" height="880" alt="Zabbix Trigger Configuration - SSH Bruteforce" src="https://github.com/user-attachments/assets/67564e32-3587-4fd6-9622-42abf801d568" />

**Trigger Logic:**
```javascript
count(//var/log/auth.log, "Failed password", "10s") > 5
```

**Trigger Properties:**
- **Name:** SSH-Bruteforce Detected
- **Severity:** High
- **Function:** `count()` with RegEx pattern
- **Condition:** >5 failures in 10 seconds

---

## 💻 Attack Simulation

### Execution from Kali Linux

<img width="1033" height="303" alt="Kali Linux - Hydra SSH Bruteforce Attack" src="https://github.com/user-attachments/assets/4e776646-acfe-4325-be23-7c192537cd58" />
 

```bash
hydra -l client1 -P /usr/share/wordlists/rockyou.txt -t 4 ssh://192.168.20.151
```

**Command Breakdown:**
- `-l client1`: Username to test
- `-P rockyou.txt`: Password dictionary file
- `-t 4`: 4 parallel connections
- `ssh://192.168.20.151`: Target SSH service

---

## 🔄 SOAR Pipeline Execution

### 1. Alert Generation

<img width="1282" height="816" alt="Zabbix Dashboard - Problem Generation" src="https://github.com/user-attachments/assets/2dc59201-3502-4d2e-b4fd-bba2aa2bc8d9" />


The alert appears in the Problems Dashboard with **High** severity, confirming the SSH-Bruteforce detection on host `ubuntu-client1`.

### 2. Webhook Transmission

<img width="1424" height="747" alt="Zabbix Action Log - Webhook Sent" src="https://github.com/user-attachments/assets/cc37a128-c7fa-4b55-960c-512ed2f1b307" />

**Action Log Details:**
- **Status:** Sent ✓
- **Type:** Shuffle Media
- **Event ID:** Captured from trigger
- **Attacker IP:** `192.168.20.152` (Internal)
- **MITRE Link:** Included in payload

### 3. Shuffle Workflow Execution

<img width="999" height="658" alt="Shuffle Workflow - Internal Threat Processing" src="https://github.com/user-attachments/assets/ee941d33-f57a-4798-92c1-a6663d518ccc" />

**Workflow Path:**
1. Entry Node (Webhook) → Received ✓
2. Python ParseToJSON → Data normalized ✓
3. Jira 4 - Confirm Private IP → Branch selected ✓
4. Slack 4 → Notification sent ✓

**Key Observation:** The workflow bypasses pfSense blocking nodes (upper branch) since the IP is classified as internal.

### 4. Execution Status

<img width="934" height="339" alt="Shuffle - Execution History" src="https://github.com/user-attachments/assets/89b56bf9-cd8a-499f-b4ee-a5bc90c2178c" />

**Execution Metrics:**
- **Status:** FINISHED ✓
- **Start Time:** 19:55:32
- **End Time:** 19:56:25
- **Total Duration:** ~53 seconds (includes human interaction time)

### 5. Raw Payload Reception

![](https://github.com/user-attachments/assets/61830bd1-6c2d-49a8-975e-9b78fc6a740f)  
<img width="571" height="313" alt="Shuffle - Webhook Payload" src="https://github.com/user-attachments/assets/4b3ed8ef-da0a-428e-a7f8-d77a3c79e5e8" />

**Payload Contains:**
- Subject: Problem: SSH-Bruteforce
- CPU Load: 58.69%
- Network traffic metrics
- MITRE ATT&CK URL
- Complete alert context

### 6. Data Normalization

<img width="577" height="417" alt="Shuffle - Python Parse Output" src="https://github.com/user-attachments/assets/a45009f8-16d4-45ba-af8f-e54a9fb5db38" />

**Parsed Data (13 items):**
```json
{
  "event_id": "1270",
  "problem_name": "SSH-Bruteforce",
  "time": "19:55:31",
  "date": "2026.06.18",
  "severity": "High",
  "ioc": "192.168.20.152",
  "host_name": "ubuntu-client1",
  "host_id": "10684",
  "host_ip": "192.168.20.151",
  "cpu_usage": "58.69",
  "inbound_traffic": "2784",
  "outbound_traffic": "3904",
  "info_url": "https://attack.mitre.org/techniques/T1110/"
}
```

---

## 📋 Jira Ticket Creation

### API Response

<img width="477" height="274" alt="Jira API - Ticket Created" src="https://github.com/user-attachments/assets/0fe4f954-c567-4710-b9e3-31de331d2017" />

**Response Details:**
- **Status:** 201 Created

### Jira Ticket View

<img width="508" height="331" alt="Jira Ticket - Internal SSH Threat" src="https://github.com/user-attachments/assets/237bde5c-477f-4413-9988-15ca062a06ec" />


**Ticket Details:**
- **Title:** [INTERNAL THREAT] SSH-Bruteforce
- **Priority:** High
- **Description includes:**
  - Event ID
  - Date/Time
  - CPU and network metrics
  - MITRE ATT&CK reference
  - Standardized investigation actions

---

## 💬 Slack Notification

### API Response

<img width="452" height="328" alt="Slack API - Notification Delivered" src="https://github.com/user-attachments/assets/8201db5d-8ebc-4cf0-91d1-f9c4c86d8dcb" />


### Slack Alert Card

<img width="515" height="193" alt="Slack - Internal Threat Notification Card" src="https://github.com/user-attachments/assets/1c130780-b0d0-4e0a-bf71-670163bc27d4" />


**Notification Content:**
- **Title:** Zabbix Alert - Intern Threat
- **IP:** `192.168.20.152` (Internal Network)
- **Host:** `ubuntu-client1` (`192.168.20.151`)
- **Alert:** SSH-Bruteforce at 19:55:31
- **MITRE Link:** Direct URL to T1110
- **Jira Ticket:** SOC-96 with direct link
- **Action Required:** Manual investigation

---

## 📊 Summary

| Step | Component | Status | Output |
|------|-----------|--------|--------|
| 1. Detection | Zabbix Trigger | ✅ Success | Alert generated |
| 2. Ingestion | Webhook (Zabbix → Shuffle) | ✅ Success | Payload sent |
| 3. Normalization | Python ParseToJSON | ✅ Success | JSON structured |
| 4. Classification | IP Type Detection | ✅ Success | Identified as Internal |
| 5. Ticketing | Jira API | ✅ Success | Ticket created |
| 6. Notification | Slack API | ✅ Success | Alert sent to SOC team |
| 7. Blocking | pfSense | ⛔ Skipped | No blocking (internal IP) |

---

## 🎯 Key Takeaways

1. **Context-Aware Response:** The SOAR correctly identified the IP as internal and avoided automatic blocking that could cause self-DoS.

2. **Comprehensive Triage:** The Jira ticket contains all relevant context for SOC analysts to begin investigation immediately.

3. **Rapid Notification:** The SOC team is alerted in ~6 seconds, significantly faster than manual notification.

4. **MITRE Integration:** The alert includes direct links to ATT&CK techniques for faster threat understanding.

5. **Analyst Empowerment:** Rather than replacing human decision-making, the SOAR augments it by handling repetitive tasks and providing rich context.

---

## 🔗 Related Resources

- [MITRE ATT&CK T1110 - Brute Force](https://attack.mitre.org/techniques/T1110/)
- [THC-Hydra Documentation](https://github.com/vanhauser-thc/thc-hydra)
- [Zabbix Log Monitoring Documentation](https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/log_items)

---

*This scenario demonstrates the effectiveness of the SOAR pipeline for internal threats, prioritizing investigation and traceability over aggressive automated blocking.*
