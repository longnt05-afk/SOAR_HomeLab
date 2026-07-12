## Ransomware Simulation MITRE ATT&CK Coverage

This ransomware simulation campaign is designed to validate endpoint, network, EDR, SIEM, and incident response visibility in the Super SOC HomeLab.

### Phase 1 - Execution
- T1059.001 - PowerShell
- T1059.003 (3-6)- Windows Command Shell

### Phase 2 - Privilege Escalation
- T1548.002 - Bypass User Account Control [Advanced / Optional]

### Phase 3 - Defense Evasion
- T1562.001 - Disable or Modify Tools
- T1070.001 - Clear Windows Event Logs
- T1036.007 - Double File Extension
- T1218.005 - Mshta [Optional]
- T1218.007 - Msiexec [Optional]
- T1218.010 - Regsvr32 [Optional]
- T1218.011 - Rundll32 [Optional]

### Phase 4 - Discovery
- T1082 - System Information Discovery
- T1057 - Process Discovery
- T1083 - File and Directory Discovery
- T1135 - Network Share Discovery
- T1016 - System Network Configuration Discovery
- T1018 - Remote System Discovery [Optional]

### Phase 5 - Collection & Exfiltration / Double Extortion
- T1560 - Archive Collected Data
- T1567.002 - Exfiltration to Cloud Storage [Optional]
- T1567.004 - Exfiltration Over Webhook [Optional]
- T1041 - Exfiltration Over C2 Channel [Optional]

### Phase 6 - Defense / Recovery Impact
- T1490 - Inhibit System Recovery
- T1489 - Service Stop

### Phase 7 - Ransomware Impact
- T1486 - Data Encrypted for Impact
- T1529 - System Shutdown/Reboot [Optional]