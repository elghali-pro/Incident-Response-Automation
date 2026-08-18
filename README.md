<div align="center">

# 🛡️ Automated Incident Response Pipeline (SOAR)

**Open-source Security Orchestration, Automation & Response platform**
*Shifting from passive monitoring to active cyber-defense*
</div>

## 📌 Overview

This project implements a fully automated **SOAR pipeline** built on **Shuffle**, designed to detect, enrich, and mitigate network threats in real time — without waiting on a human analyst to act first.

Alerts, raised by **Zabbix** and **Snort**, are automatically parsed, cross-checked against threat intelligence feeds, and — when confirmed malicious — remediated directly on the firewall, with full traceability through Jira and Slack.

<div align="center">

| Metric | Manual Response | Automated (This Project) | Improvement |
|:---:|:---:|:---:|:---:|
| **Mean Time to Respond (MTTR)** | ~15 minutes | **~1 minute** | **~93% faster** |

</div>



## 🚀 Key Features

| Feature | Description |
|---|---|
| 🔄 **Automated Ingestion** | Real-time alert collection from Zabbix via secure HTTP POST webhooks |
| 🧹 **Data Normalization** | Custom Python regex parsing to transform raw logs into structured JSON |
| 🔍 **Threat Intelligence Enrichment** | Live IP reputation checks via VirusTotal & AbuseIPDB APIs |
| 🧠 **Contextual Decision Making** | Automatic segregation between internal (private) and external (public) threats |
| 🔥 **Active Remediation** | Automated IP blocking on the **pfSense** firewall via REST API |
| 📋 **Full Traceability** | Automatic Jira ticket lifecycle management and rich Slack notifications |



## 🛠️ Tech Stack

<table>
<tr>
<td><b>Orchestration</b></td>
<td><img src="https://img.shields.io/badge/Shuffle-SOAR-orange?logo=shuffle&logoColor=white"></td>
</tr>
<tr>
<td><b>Monitoring & IDS</b></td>
<td>
<img src="https://img.shields.io/badge/Zabbix-CC0000?logo=zabbix&logoColor=white">
<img src="https://img.shields.io/badge/Snort-IDS-red?logo=snort&logoColor=white">
</td>
</tr>
<tr>
<td><b>Firewall</b></td>
<td><img src="https://img.shields.io/badge/pfSense-212121?logo=pfsense&logoColor=white"></td>
</tr>
<tr>
<td><b>Languages</b></td>
<td>
<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black">
<img src="https://img.shields.io/badge/PHP-777BB4?logo=php&logoColor=white"></td>
</tr>
<tr>
<td><b>Ticketing & Notifications</b></td>
<td>
<img src="https://img.shields.io/badge/Jira-0052CC?logo=jira&logoColor=white">
<img src="https://img.shields.io/badge/Slack%20API-4A154B?logo=slack&logoColor=white">
</td>
</tr>
<tr>
<td><b>Environment</b></td>
<td>
<img src="https://img.shields.io/badge/Proxmox%20VE-E57000?logo=proxmox&logoColor=white">
<img src="https://img.shields.io/badge/Debian%2013-A81D33?logo=debian&logoColor=white">
<img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white">
</td>
</tr>
</table>



## 📐 Architecture & Logic

### Lab Architecture
<p align="center">
<img width="500" height="700" alt="SOC Lab Architecture" src="https://github.com/user-attachments/assets/a3014130-f351-4999-9d73-99e5c955d616" />
</p>

### Threat Flow (Logical Mitigation)
<p align="center">
<img width="500" height="600" alt="SOAR Pipeline Logic Process" src="https://github.com/user-attachments/assets/e8adea6c-0381-4d2a-9fb8-4ef1a651451c" />
</p>

### SOAR Pipeline
<p align="center">
<img width="500" height="300" alt="SOAR Pipeline" src="https://github.com/user-attachments/assets/c87b1887-26d0-43c7-9a38-3859ecb5be6c" />
</p>



## 📋 How It Works — Example Scenario

1. **Detection** — An external attack occurs; Zabbix raises a high-severity trigger and forwards the payload to Shuffle.
2. **Enrichment** — Shuffle parses the payload and queries VirusTotal, identifying a malicious reputation score.
3. **Remediation** — Shuffle instructs pfSense to block the offending IP.
4. **Closure** — The Zabbix alert is closed, a "Done" ticket is logged in Jira, and the SOC team is pinged via Slack — all within roughly a minute of detection.

---

<div align="center">

*Built as part of a graduation project (PFE) focused on SOC/SOAR architecture and automated threat response.*

</div>
