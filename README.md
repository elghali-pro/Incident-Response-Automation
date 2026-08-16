# Automated Incident Response Pipeline (SOAR)

## 📌 Project Overview
This project focuses on shifting from passive monitoring to active cyber-defense. It implements an open-source SOAR (Security Orchestration, Automation, and Response) architecture using **Shuffle** to automatically mitigate network threats detected by **Zabbix & Snort**.

**Key Achievement:** Reduced the Mean Time to Respond (MTTR) from 15 minutes (manual) to **around 1 minute** (automated).

## 🚀 Key Features
- **Automated Ingestion:** Real-time alert collection from Zabbix via secure HTTP POST Webhooks.
- **Data Normalization:** Custom Python regex parsing to transform raw logs into structured JSON data.
- **Threat Intelligence Enrichment:** Live IP reputation checking via VirusTotal & AbuseIPDB APIs.
- **Contextual Decision Making:** Intelligent segregation between internal (private) and external (public) threats.
- **Active Remediation:** Automated IP blocking on **pfSense** firewall using REST APIs.
- **Full Traceability:** Automatic Jira ticket lifecycle management and rich Slack notifications.

## 🛠️ Tech Stack

**Orchestration** \
![Shuffle](https://img.shields.io/badge/Shuffle-SOAR-orange?logo=shuffle&logoColor=white)

**Monitoring & IDS**\
![Zabbix](https://img.shields.io/badge/Zabbix-CC0000?logo=zabbix&logoColor=white)
![Snort](https://img.shields.io/badge/Snort-IDS-red?logo=snort&logoColor=white)

**Firewall**\
![pfSense](https://img.shields.io/badge/pfSense-212121?logo=pfsense&logoColor=white)

**Languages**\
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

**Ticketing & Team Notification**\
![Jira](https://img.shields.io/badge/Jira-0052CC?logo=jira&logoColor=white)
![Slack](https://img.shields.io/badge/Slack%20API-4A154B?logo=slack&logoColor=white)

**Environment**\
![Proxmox](https://img.shields.io/badge/Proxmox%20VE-E57000?logo=proxmox&logoColor=white)
![Debian](https://img.shields.io/badge/Debian%2013-A81D33?logo=debian&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

## 📐 Architecture & Logic
### Lab Architecture
<img width="821" height="1031" alt="SOC-Lab-Architecture" src="https://github.com/user-attachments/assets/a3014130-f351-4999-9d73-99e5c955d616" />


### Threat Flow (Logical Mitigation)
<img width="448" height="600" alt="SOAR-pipeline-logic-process" src="https://github.com/user-attachments/assets/e8adea6c-0381-4d2a-9fb8-4ef1a651451c" />


### SOAR Pipeline
<img width="538" height="334" alt="SOAR-pipeline" src="https://github.com/user-attachments/assets/c87b1887-26d0-43c7-9a38-3859ecb5be6c" />


## 📋 How It Works (Example)
1. An external attack occurs.
2. Zabbix raises a high-severity trigger and forwards the payload to Shuffle.
3. Shuffle parses the text block, queries VirusTotal, and identifies a malicious score.
4. Shuffle instructs pfSense to block the IP, closes the Zabbix alert, logs a 'Done' ticket in Jira, and pings the SOC team via Slack.
