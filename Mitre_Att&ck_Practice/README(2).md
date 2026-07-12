# MITRE ATT&CK Practice – Super SOC HomeLab

Thư mục này được dùng để thực hành, kiểm thử và ghi nhận các kỹ thuật MITRE ATT&CK trong bài lab **Super SOC HomeLab**.

Mục tiêu chính của thư mục là lưu lại các test case, ghi chú điều tra, truy vấn Splunk, bằng chứng log và kết quả phát hiện từ các nguồn như:

- Sysmon / Windows Event Log
- LimaCharlie EDR
- Zeek NSM
- Suricata IDS/IPS
- pfSense Firewall
- Splunk SIEM
- DFIR-IRIS Case Management

## Mục tiêu thực hành

Các bài thực hành trong thư mục này tập trung vào việc kiểm tra khả năng phát hiện và điều tra các hành vi tấn công mô phỏng theo MITRE ATT&CK, bao gồm:

- Execution
- Persistence
- Privilege Escalation
- Defense Evasion
- Credential Access
- Discovery
- Lateral Movement
- Command and Control
- Exfiltration
- Impact

## Công cụ sử dụng

Một số công cụ có thể được dùng trong quá trình practice:

- Atomic Red Team
- Invoke-AtomicRedTeam
- LimaCharlie EDR
- Sysmon
- Splunk Enterprise
- Zeek
- Suricata
- DFIR-IRIS

## Cấu trúc đề xuất

```text
MITRE-ATTACK-Practice/
├── README.md
├── T1059.001-PowerShell/
│   ├── notes.md
│   ├── splunk-queries.md
│   ├── evidence/
│   └── report.md
├── T1105-Ingress-Tool-Transfer/
│   ├── notes.md
│   ├── splunk-queries.md
│   ├── evidence/
│   └── report.md
└── T1003-Credential-Dumping/
    ├── notes.md
    ├── splunk-queries.md
    ├── evidence/
    └── report.md
```

## Quy trình thực hành mỗi kỹ thuật

Mỗi kỹ thuật nên được ghi lại theo quy trình:

1. Chọn kỹ thuật MITRE ATT&CK cần test.
2. Chạy test case bằng Atomic Red Team hoặc công cụ mô phỏng phù hợp.
3. Thu thập log từ Sysmon, EDR, Zeek, Suricata hoặc pfSense.
4. Phân tích log trong Splunk.
5. Xác định các bằng chứng chính:
   - Process
   - Parent process
   - Command line
   - User
   - Host
   - Network connection
   - DNS query
   - EDR detection
6. Mapping kỹ thuật với MITRE ATT&CK.
7. Viết kết luận điều tra.
8. Đề xuất detection rule hoặc cải thiện rule hiện có.
9. Lưu screenshot và SPL query vào thư mục evidence.

## Mẫu thông tin cần ghi cho mỗi test case

```text
Technique ID:
Technique Name:
Tactic:
Tool Used:
Target Host:
Target IP:
Time Window:
Command Executed:
Data Sources:
Detection Result:
Severity:
Verdict:
MITRE Mapping:
Lessons Learned:
```

## Ví dụ test case

```text
Technique ID: T1059.001
Technique Name: PowerShell
Tactic: Execution
Tool Used: Atomic Red Team
Target Host: Windows 10 Victim
Data Sources: Sysmon, LimaCharlie EDR, Splunk
Detection Result: Sysmon Event ID 1, 3, 22 and LimaCharlie PowerShell detections
Verdict: True Positive - Authorized Simulation
```

## Ghi chú an toàn

Các bài thực hành trong thư mục này chỉ được thực hiện trong môi trường lab cô lập và có kiểm soát. Không chạy test case trên hệ thống thật, hệ thống không thuộc quyền quản lý, hoặc môi trường production.

Trước khi chạy các test có khả năng thay đổi hệ thống như persistence, credential dumping, defense evasion hoặc impact, cần tạo snapshot máy ảo để có thể khôi phục trạng thái ban đầu.

## Mục tiêu cuối cùng

Thư mục này giúp chứng minh năng lực xây dựng và vận hành một quy trình SOC thực tế:

```text
Attack Simulation
        ↓
Telemetry Collection
        ↓
Detection Engineering
        ↓
SIEM Correlation
        ↓
Incident Triage
        ↓
Case Management
        ↓
Reporting
```

Đây là một phần của dự án **Super SOC HomeLab**, nhằm rèn luyện kỹ năng SOC Analyst, Detection Engineering và Incident Response.
