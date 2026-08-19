# Zabbix Dashboard Configuration & UserParameters

## 📊 Dashboard Overview

![Zabbix SOAR Dashboard](https://github.com/user-attachments/assets/abc123def456)  
*Figure 7.51 – SOAR Dashboard implemented in Zabbix*

---

## 📁 File Structure

```
zen-networks-soar/
├── dashboards/
│   ├── zabbix-dashboard-template.yaml           # Dashboard export
│   ├── zabbix-userparameters.conf               # UserParameters configuration
│   ├── dashboard-screenshot.png                 # Dashboard screenshot
│   └── README.md                                # Dashboard documentation
│
├── orchestration/
│   └── zabbix/
│       ├── user-parameters/
│       │   └── zabbix-userparameters.conf       # Main UserParameter file
│       └── templates/
│           └── zabbix-dashboard-template.xml    # Dashboard XML export
│
└── docs/
    └── dashboard-guide.md                        # Setup and usage guide
```

---

## 🔧 Zabbix UserParameters

### `zabbix-userparameters.conf`

```bash
# ============================================================================ #
# Zabbix Agent UserParameters - SOAR Dashboard Metrics
# ============================================================================ #
# Description: Custom UserParameters for SOAR dashboard metrics
# Author: Zen Networks SOAR Team
# Version: 1.0.0
# Location: /etc/zabbix/zabbix_agentd.d/userparameters.conf
# ============================================================================ #

# ---------------------------------------------------------------------------- #
# Database Connection Configuration
# ---------------------------------------------------------------------------- #
# MySQL credentials file must be configured at:
# /var/lib/zabbix/.my.cnf
#
# Example .my.cnf:
# [client]
# user=zabbix
# password=your_password
# host=localhost
# ---------------------------------------------------------------------------- #

# ============================================================================ #
# 1. PROBLEM COUNT METRICS
# ============================================================================ #

# ------------------------------------------------------------
# Total Problems Generated (All Time)
# Description: Total number of problems ever generated
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.total.generated,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=1"

# ------------------------------------------------------------
# Total Problems Resolved (All Time)
# Description: Total number of problems resolved
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.total.resolved,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=0 AND e.acknowledged=1"

# ------------------------------------------------------------
# Total Active Problems (High Severity)
# Description: Currently active problems with High severity
# Type: Current Value
# ------------------------------------------------------------
UserParameter=zabbix.active.problems.high,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM problem WHERE severity=4 AND r_eventid IS NULL"

# ------------------------------------------------------------
# Total Active Problems (All Severities)
# Description: Currently active problems (all severities)
# Type: Current Value
# ------------------------------------------------------------
UserParameter=zabbix.active.problems.total,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM problem WHERE r_eventid IS NULL"

# ============================================================================ #
# 2. SPECIFIC PROBLEM TYPE METRICS
# ============================================================================ #

# ------------------------------------------------------------
# Total SSH-Bruteforce Problems Generated
# Description: Count of SSH-Bruteforce incidents
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.count.SSH-Bruteforce,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=1 AND t.description LIKE '%SSH-Bruteforce%'"

# ------------------------------------------------------------
# Total Network-Port-Scan Problems Generated
# Description: Count of Network-Port-Scan incidents
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.count.Network-Port-Scan,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=1 AND t.description LIKE '%Network-Port-Scan%'"

# ------------------------------------------------------------
# Total Protocol-Mismatch Problems Generated
# Description: Count of Protocol-Mismatch incidents
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.count.Protocol-Mismatch,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=1 AND t.description LIKE '%Protocol-Mismatch%'"

# ------------------------------------------------------------
# Total SSH-Bruteforce Problems Resolved
# Description: Count of resolved SSH-Bruteforce incidents
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.resolved.count.SSH-Bruteforce,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=0 AND e.acknowledged=1 AND t.description LIKE '%SSH-Bruteforce%'"

# ------------------------------------------------------------
# Total Network-Port-Scan Problems Resolved
# Description: Count of resolved Network-Port-Scan incidents
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.resolved.count.Network-Port-Scan,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=0 AND e.acknowledged=1 AND t.description LIKE '%Network-Port-Scan%'"

# ------------------------------------------------------------
# Total Protocol-Mismatch Problems Resolved
# Description: Count of resolved Protocol-Mismatch incidents
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.resolved.count.Protocol-Mismatch,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=0 AND e.acknowledged=1 AND t.description LIKE '%Protocol-Mismatch%'"

# ============================================================================ #
# 3. DAILY METRICS
# ============================================================================ #

# ------------------------------------------------------------
# Total Problems Generated Today
# Description: Problems generated in the last 24 hours
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.total.generated.daily,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=1 AND e.clock >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 1 DAY))"

# ------------------------------------------------------------
# Total Problems Resolved Today
# Description: Problems resolved in the last 24 hours
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.trigger.total.resolved.daily,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=0 AND e.acknowledged=1 AND e.clock >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 1 DAY))"

# ============================================================================ #
# 4. SOAR PERFORMANCE METRICS
# ============================================================================ #

# ------------------------------------------------------------
# Average Response Time (Manual vs Automated)
# Description: Calculates average MTTR for SOAR-automated incidents
# Type: Calculated
# ------------------------------------------------------------
UserParameter=zabbix.soar.avg.response.time,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT AVG(TIMESTAMPDIFF(SECOND, FROM_UNIXTIME(e.clock), FROM_UNIXTIME(e.acknowledged_at))) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=0 AND e.acknowledged=1 AND t.description LIKE '%Protocol-Mismatch%' OR t.description LIKE '%Network-Port-Scan%'"

# ------------------------------------------------------------
# Total Automated Actions (SOAR Interventions)
# Description: Count of incidents handled by Shuffle
# Type: Counter
# ------------------------------------------------------------
UserParameter=zabbix.soar.total.actions,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM events e JOIN triggers t ON e.objectid=t.triggerid WHERE e.source=0 AND e.object=0 AND e.value=0 AND e.acknowledged=1 AND e.acknowledged_by=1 AND (t.description LIKE '%Protocol-Mismatch%' OR t.description LIKE '%Network-Port-Scan%')"

# ============================================================================ #
# 5. HOST AVAILABILITY METRICS
# ============================================================================ #

# ------------------------------------------------------------
# Total Hosts Available
# Description: Number of hosts currently available
# Type: Current Value
# ------------------------------------------------------------
UserParameter=zabbix.hosts.available,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM hosts h JOIN host_availability ha ON h.hostid=ha.hostid WHERE h.status=0 AND ha.available=1"

# ------------------------------------------------------------
# Total Hosts Unavailable
# Description: Number of hosts currently unavailable
# Type: Current Value
# ------------------------------------------------------------
UserParameter=zabbix.hosts.unavailable,mysql --defaults-extra-file=/var/lib/zabbix/.my.cnf zabbix -N -e "SELECT COUNT(*) FROM hosts h JOIN host_availability ha ON h.hostid=ha.hostid WHERE h.status=0 AND ha.available=0"
```

---

## 📊 Zabbix Dashboard Template

### `zabbix-dashboard-template.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<zabbix_export>
    <version>7.0</version>
    <date>2026-06-19T11:00:00Z</date>
    <dashboard>
        <name>SOAR Security Dashboard</name>
        <display_period>1h</display_period>
        <auto_start_slideshow>0</auto_start_slideshow>
        <refresh_mode>0</refresh_mode>
        <refresh_interval>30</refresh_interval>
        <dashboardid>10001</dashboardid>
        <userid>1</userid>
        
        <!-- A. Total Incidents Generated -->
        <widget>
            <type>item</type>
            <name>Total Incidents Generated</name>
            <width>250</width>
            <height>120</height>
            <x>0</x>
            <y>0</y>
            <fields>
                <field>
                    <name>itemid</name>
                    <value>12345</value>
                </field>
                <field>
                    <name>items</name>
                    <value>zabbix.trigger.total.generated</value>
                </field>
                <field>
                    <name>show</name>
                    <value>3</value>
                </field>
                <field>
                    <name>style</name>
                    <value>1</value>
                </field>
            </fields>
        </widget>
        
        <!-- B. Total Active Incidents -->
        <widget>
            <type>item</type>
            <name>Active Incidents</name>
            <width>250</width>
            <height>120</height>
            <x>250</x>
            <y>0</y>
            <fields>
                <field>
                    <name>itemid</name>
                    <value>12346</value>
                </field>
                <field>
                    <name>items</name>
                    <value>zabbix.active.problems.total</value>
                </field>
                <field>
                    <name>show</name>
                    <value>3</value>
                </field>
                <field>
                    <name>style</name>
                    <value>1</value>
                </field>
            </fields>
        </widget>
        
        <!-- C. Total Resolved Incidents -->
        <widget>
            <type>item</type>
            <name>Resolved Incidents</name>
            <width>250</width>
            <height>120</height>
            <x>500</x>
            <y>0</y>
            <fields>
                <field>
                    <name>itemid</name>
                    <value>12347</value>
                </field>
                <field>
                    <name>items</name>
                    <value>zabbix.trigger.total.resolved</value>
                </field>
                <field>
                    <name>show</name>
                    <value>3</value>
                </field>
                <field>
                    <name>style</name>
                    <value>1</value>
                </field>
            </fields>
        </widget>
        
        <!-- D. Host Availability -->
        <widget>
            <type>item</type>
            <name>Hosts Available</name>
            <width>250</width>
            <height>120</height>
            <x>750</x>
            <y>0</y>
            <fields>
                <field>
                    <name>itemid</name>
                    <value>12348</value>
                </field>
                <field>
                    <name>items</name>
                    <value>zabbix.hosts.available</value>
                </field>
                <field>
                    <name>show</name>
                    <value>3</value>
                </field>
                <field>
                    <name>style</name>
                    <value>1</value>
                </field>
            </fields>
        </widget>
        
        <!-- F. Attack Distribution Pie Chart -->
        <widget>
            <type>pie</type>
            <name>Attack Distribution</name>
            <width>300</width>
            <height>250</height>
            <x>0</x>
            <y>120</y>
            <fields>
                <field>
                    <name>items</name>
                    <value>
                        zabbix.trigger.count.SSH-Bruteforce,
                        zabbix.trigger.count.Network-Port-Scan,
                        zabbix.trigger.count.Protocol-Mismatch
                    </value>
                </field>
                <field>
                    <name>title</name>
                    <value>Attack Types</value>
                </field>
            </fields>
        </widget>
        
        <!-- G. Daily Alert Trend -->
        <widget>
            <type>graph</type>
            <name>Daily Alert Trend</name>
            <width>650</width>
            <height>250</height>
            <x>300</x>
            <y>120</y>
            <fields>
                <field>
                    <name>items</name>
                    <value>
                        zabbix.trigger.total.generated.daily,
                        zabbix.trigger.total.resolved.daily
                    </value>
                </field>
                <field>
                    <name>title</name>
                    <value>Alert Trend (24 hours)</value>
                </field>
            </fields>
        </widget>
        
        <!-- H. Problem History -->
        <widget>
            <type>problems</type>
            <name>Problem History</name>
            <width>950</width>
            <height>250</height>
            <x>0</x>
            <y>370</y>
            <fields>
                <field>
                    <name>show</name>
                    <value>1</value>
                </field>
                <field>
                    <name>title</name>
                    <value>Recent Security Problems</value>
                </field>
            </fields>
        </widget>
        
        <!-- I. Webhook History -->
        <widget>
            <type>item</type>
            <name>Messages Sent to Shuffle</name>
            <width>950</width>
            <height>120</height>
            <x>0</x>
            <y>620</y>
            <fields>
                <field>
                    <name>items</name>
                    <value>zabbix.webhook.sent.count</value>
                </field>
                <field>
                    <name>show</name>
                    <value>3</value>
                </field>
                <field>
                    <name>style</name>
                    <value>1</value>
                </field>
            </fields>
        </widget>
    </dashboard>
</zabbix_export>
```

---

## 🖥️ Dashboard Widgets Description

| Widget | Label | Metric | Description |
|--------|-------|--------|-------------|
| **A** | Total Incidents Generated | `zabbix.trigger.total.generated` | Counter of all problems ever created |
| **B** | Active Incidents | `zabbix.active.problems.total` | Currently open problems (all severities) |
| **C** | Resolved Incidents | `zabbix.trigger.total.resolved` | Counter of all resolved problems |
| **D** | Hosts Available | `zabbix.hosts.available` | Number of hosts currently available |
| **E** | Topology | - | Network connectivity visualization |
| **F** | Attack Distribution | Pie Chart | Breakdown by attack type (SSH, Scan, Protocol) |
| **G** | Daily Alert Trend | Graph | 24-hour trend of generated vs resolved |
| **H** | Problem History | List | Recent security incidents with details |
| **I** | Webhook History | - | Messages sent to Shuffle SOAR |

---

## 📋 MySQL Credentials File

### `/var/lib/zabbix/.my.cnf`

```ini
[client]
user=zabbix
password=your_zabbix_database_password
host=localhost
socket=/var/run/mysqld/mysqld.sock
```

**Set proper permissions:**
```bash
chmod 600 /var/lib/zabbix/.my.cnf
chown zabbix:zabbix /var/lib/zabbix/.my.cnf
```

---

## 🚀 Installation Instructions

### 1. Configure UserParameters

```bash
# Copy the userparameters file
sudo cp zabbix-userparameters.conf /etc/zabbix/zabbix_agentd.d/

# Test the parameters
zabbix_agentd -t zabbix.trigger.total.generated
zabbix_agentd -t zabbix.trigger.count.SSH-Bruteforce

# Restart Zabbix agent
sudo systemctl restart zabbix-agent
```

### 2. Test Individual UserParameters

```bash
# Test from Zabbix server
zabbix_get -s 192.168.10.150 -k "zabbix.trigger.total.generated"
zabbix_get -s 192.168.10.150 -k "zabbix.trigger.count.SSH-Bruteforce"
zabbix_get -s 192.168.10.150 -k "zabbix.active.problems.total"
zabbix_get -s 192.168.10.150 -k "zabbix.hosts.available"
```

### 3. Import Dashboard Template

1. Login to Zabbix Web UI
2. Go to **Dashboards** → **Import**
3. Upload `zabbix-dashboard-template.xml`
4. Map existing hosts and items
5. Save and view dashboard

---

## 📊 Dashboard Metrics Explanation

### Dashboard Widgets from Figure 7.51

| Widget Label | Description | Data Source |
|-------------|-------------|-------------|
| **A** | Total number of security problems generated | `zabbix.trigger.total.generated` |
| **B** | Total number of active (unresolved) problems | `zabbix.active.problems.total` |
| **C** | Total number of resolved problems | `zabbix.trigger.total.resolved` |
| **D** | Host availability status | `zabbix.hosts.available` |
| **E** | Network topology visualization | Built-in Zabbix topology |
| **F** | Attack type distribution (pie chart) | Custom item queries |
| **G** | Daily alert trend (24h) | `zabbix.trigger.total.generated.daily` |
| **H** | Recent security incidents list | Zabbix Problems widget |
| **I** | Webhook messages sent to Shuffle | `zabbix.webhook.sent.count` |

---

## 🔍 Query Reference

### Count Problems by Host

```sql
SELECT h.host, COUNT(*) as problem_count 
FROM events e 
JOIN triggers t ON e.objectid = t.triggerid 
JOIN hosts h ON t.hostid = h.hostid 
WHERE e.source = 0 AND e.object = 0 AND e.value = 1 
GROUP BY h.host 
ORDER BY problem_count DESC;
```

### MTTR Calculation

```sql
SELECT 
    AVG(TIMESTAMPDIFF(MINUTE, 
        FROM_UNIXTIME(e.clock), 
        FROM_UNIXTIME(e.acknowledged_at)
    )) as avg_mttr_minutes
FROM events e 
JOIN triggers t ON e.objectid = t.triggerid 
WHERE e.source = 0 AND e.object = 0 
AND e.value = 0 AND e.acknowledged = 1;
```

---

## 📁 File Structure

```
zen-networks-soar/
├── dashboards/
│   ├── zabbix-dashboard-template.yaml           # Dashboard export
│   ├── zabbix-userparameters.conf               # UserParameters configuration
│   ├── dashboard-screenshot.png                 # Dashboard screenshot
│   └── README.md                                # This documentation
│
├── orchestration/
│   └── zabbix/
│       ├── user-parameters/
│       │   └── zabbix-userparameters.conf       # Main UserParameter file
│       ├── templates/
│       │   └── zabbix-dashboard-template.xml    # Dashboard XML export
│       └── .my.cnf.example                      # MySQL credentials template
│
└── docs/
    └── dashboard-guide.md                       # Setup and usage guide
```

---

## 🎯 Summary

| Metric | UserParameter | Type | Purpose |
|--------|--------------|------|---------|
| Total Generated | `zabbix.trigger.total.generated` | Counter | Overall incident count |
| Active Problems | `zabbix.active.problems.total` | Current | Open incidents |
| Resolved Problems | `zabbix.trigger.total.resolved` | Counter | Closed incidents |
| SSH Count | `zabbix.trigger.count.SSH-Bruteforce` | Counter | SSH attack tracking |
| Scan Count | `zabbix.trigger.count.Network-Port-Scan` | Counter | Port scan tracking |
| Protocol Count | `zabbix.trigger.count.Protocol-Mismatch` | Counter | External threat tracking |
| Daily Generated | `zabbix.trigger.total.generated.daily` | Counter | 24h trend |
| Daily Resolved | `zabbix.trigger.total.resolved.daily` | Counter | 24h resolution trend |
| Host Availability | `zabbix.hosts.available` | Current | Infrastructure health |