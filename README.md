# 🛡️ SuperSOAR HomeLab

> **Xây dựng hệ thống SIEM + SOAR tự động hóa ứng phó sự cố với tích hợp AI**  
> Mở rộng nâng cao từ bài lab pfSense, bổ sung các tầng phòng thủ SIEM · SOAR · Threat Intelligence · AI-Powered Analysis

## 🔍 Tổng Quan

**SuperSOAR HomeLab** là một hệ thống bảo mật lab mô phỏng môi trường SOC (Security Operations Center) doanh nghiệp thực tế, được triển khai trên VMware Workstation.

Bài lab giải quyết bài toán: **"Làm thế nào để một SOC Analyst phát hiện và ứng phó với mối đe dọa nhanh nhất có thể mà không cần can thiệp thủ công 24/7?"**

Giải pháp: xây dựng pipeline tự động hoàn chỉnh từ thu thập log → phát hiện bất thường → làm giàu Threat Intelligence → phân tích AI → cảnh báo real-time, phản hồi trong vòng **dưới 60 giây**.

---

## ✨ Tính Năng Chính

| # | Tính Năng | Mô Tả |
|---|-----------|--------|
| 1 | **SIEM tập trung** | Splunk thu thập log từ Firewall, Endpoint, PowerShell vào 3 index riêng biệt |
| 2 | **Endpoint Monitoring** | Sysmon giám sát chi tiết tiến trình, kết nối mạng, registry, DNS trên Windows 10 |
| 3 | **Tự động hóa ứng phó** | n8n SOAR điều phối toàn bộ workflow, không cần can thiệp thủ công |
| 4 | **Threat Intelligence** | Tự động tra cứu IP qua AbuseIPDB và file hash qua VirusTotal |
| 5 | **AI Security Analyst** | Google Gemini phân tích ngữ cảnh, gán nhãn 🔴🟡🟢, viết báo cáo tiếng Việt |
| 6 | **Real-time Alert** | Telegram Bot gửi cảnh báo đầy đủ đến SOC trong vòng dưới 60 giây |
| 7 | **Defense-in-Depth** | 7 lớp phòng thủ độc lập từ Perimeter đến AI Analysis |

---

## 🏗️ Kiến Trúc Hệ Thống

![Network Architecture](Screenshot_2026-06-22_111631.png)

Hệ thống được phân tách thành **3 vùng mạng độc lập** với pfSense làm trung tâm điều phối:

### Vùng LAN — `172.16.1.0/24`
| Thiết Bị | IP | Vai Trò |
|----------|-----|---------|
| Windows 10 VM | `172.16.1.10` | Endpoint giám sát — Sysmon + Splunk Universal Forwarder |
| Ubuntu Server | `172.16.1.20` | Splunk Enterprise SIEM |
| Ubuntu Server | `172.16.1.30` | n8n SOAR Automation |

### Vùng DMZ — `10.0.0.0/24`
| Thiết Bị | IP | Vai Trò |
|----------|-----|---------|
| Windows Server 2012 R2 | `10.0.0.20` | MDaemon Mail Server, DNS, IIS Web |

### Vùng WAN — `192.168.168.0/24`
| Thiết Bị | IP | Vai Trò |
|----------|-----|---------|
| pfSense Firewall | `192.168.168.157` | NAT, Firewall, Suricata IDS/IPS |
| Kali Linux (Attacker) | `192.168.168.154` | Máy tấn công mô phỏng |

---

## 🔄 SOAR Workflow

![n8n SOAR Workflow](Screenshot_2026-06-22_105910.png)

Workflow n8n nhận Webhook từ Splunk và phân luồng tự động qua Switch node:

```
Splunk Alert
    │
    ▼
Webhook (POST)
    │
    ▼
Switch Node ──── Rule 0 ──► HTTP Request (AbuseIPDB) ──► Gemini AI ──┐
                │                                                      │
                ├─── Rule 1 ──► Code JS (Extract SHA256)              │
                │               └──► VirusTotal API ──► Gemini AI ───┤──► Telegram
                │                                                      │
                └─── Rule 2 ──► Gemini AI (PowerShell Analysis) ──────┘
```

---

## 🎯 3 Use Cases

### 🌐 Use Case 1 — Network Threat Detection (Nhánh 0)

```
pfSense filterlog ──► Splunk Alert (IP bị block > 50 lần/phút)
    ──► n8n ──► AbuseIPDB API ──► Gemini phân tích ──► Telegram 🔴🟡🟢
```

- **Nguồn log:** pfSense Firewall + Suricata IDS
- **Phát hiện:** Port scanning, brute force — IP bị chặn > 50 lần trong 1 phút
- **Threat Intel:** AbuseIPDB (reputation score, quốc gia, ISP, loại tấn công)
- **MITRE ATT&CK:** T1595.001 — Active Scanning

---

### 💻 Use Case 2 — Endpoint Threat Detection (Nhánh 1)

```
Sysmon Event ID 1 ──► Splunk Alert (LOLBin process detected)
    ──► n8n ──► Extract SHA256 (Regex) ──► VirusTotal ──► Gemini ──► Telegram 🔴🟡🟢
```

- **Nguồn log:** Sysmon Operational (Event ID 1 — Process Creation)
- **Phát hiện:** Living off the Land Binaries — `certutil`, `bitsadmin`, `mshta`, `rundll32`, `regsvr32`
- **Threat Intel:** VirusTotal (70+ AV engine scan theo SHA256 hash)
- **MITRE ATT&CK:** T1105 (Ingress Tool Transfer), T1218 (System Binary Proxy Execution)

---

### ⚡ Use Case 3 — PowerShell Threat Detection (Nhánh 2)

```
PowerShell Event ID 4104 ──► Splunk Alert (Encoded/Obfuscated PS detected)
    ──► n8n ──► Gemini (decode Base64 + phân tích) ──► Telegram 🔴🟡🟢
```

- **Nguồn log:** PowerShell Operational (Event ID 4104 — ScriptBlock Logging)
- **Phát hiện:** `-EncodedCommand`, `IEX`, `Invoke-Expression`, `Net.WebClient`, `DownloadString`
- **Đặc điểm:** Windows tự decode Base64 trước khi ghi log → AI luôn thấy nội dung thật dù attacker obfuscate bao nhiêu lớp
- **MITRE ATT&CK:** T1059.001 (PowerShell), T1027 (Obfuscated Files)

---

### 🏷️ Hệ Thống Nhãn Cảnh Báo

| Nhãn | Mức Độ | Điều Kiện | Hành Động |
|------|--------|-----------|-----------|
| 🔴 ĐỎ | Nguy hiểm cao | AbuseScore > 80 / VT > 5 engine / C2 rõ ràng | Cách ly ngay, điều tra forensic |
| 🟡 VÀNG | Đáng ngờ | AbuseScore 30–80 / VT 1–5 engine | Theo dõi chặt, thu thập thêm bằng chứng |
| 🟢 XANH | Bình thường | AbuseScore < 30 / VT = 0 engine | Ghi nhận, tiếp tục giám sát |

---

## 🛠️ Công Nghệ Sử Dụng

| Công Nghệ | Phiên Bản | Vai Trò |
|-----------|-----------|---------|
| ![Splunk](https://img.shields.io/badge/Splunk-000000?style=flat&logo=splunk&logoColor=white) Splunk Enterprise | 10.4.0 | SIEM — thu thập, tìm kiếm, alert |
| ![pfSense](https://img.shields.io/badge/pfSense-212121?style=flat&logo=pfsense&logoColor=white) pfSense | 2.7.x | Firewall, NAT, phân vùng mạng |
| ![Suricata](https://img.shields.io/badge/Suricata-EF3B2D?style=flat) Suricata | 7.x | IDS/IPS — phát hiện tấn công Layer 7 |
| ![Sysmon](https://img.shields.io/badge/Sysmon-0078D4?style=flat&logo=windows&logoColor=white) Sysmon | 15.x | Endpoint monitoring chi tiết |
| ![n8n](https://img.shields.io/badge/n8n-EA4B71?style=flat&logo=n8n&logoColor=white) n8n | LTS | SOAR — tự động hóa workflow |
| ![AbuseIPDB](https://img.shields.io/badge/AbuseIPDB-CC0000?style=flat) AbuseIPDB | v2 API | Threat Intel — IP reputation |
| ![VirusTotal](https://img.shields.io/badge/VirusTotal-394EFF?style=flat) VirusTotal | v3 API | Threat Intel — file hash analysis |
| ![Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=flat&logo=google&logoColor=white) Google Gemini | API | AI Analyst — phân tích + gán nhãn |
| ![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white) Telegram Bot | API | Kênh cảnh báo real-time |
| ![VMware](https://img.shields.io/badge/VMware-607078?style=flat&logo=vmware&logoColor=white) VMware Workstation | 17.x | Hypervisor — môi trường lab |

---

## 🌐 Cấu Hình Mạng

```
Internet / WAN (192.168.168.0/24)
        │
        │ NAT
        ▼
┌───────────────────────────────┐
│   pfSense Firewall            │
│   WAN: 192.168.168.157        │
│   LAN: 172.16.1.1             │
│   DMZ: 10.0.0.1               │
│   + Suricata IDS/IPS          │
└──────────┬──────────┬─────────┘
           │          │
     VMnet2│          │VMnet3
           ▼          ▼
   ┌──────────┐  ┌──────────┐
   │   LAN    │  │   DMZ    │
   │172.16.1.x│  │10.0.0.x  │
   │          │  │          │
   │ Win10    │  │WinSrv2012│
   │ Splunk   │  │MDaemon   │
   │ n8n      │  │DNS / IIS │
   └──────────┘  └──────────┘
```

### Bảng Phân Vùng VMware

| VMnet | Vùng | Subnet | Interface pfSense |
|-------|------|--------|-------------------|
| VMnet2 | LAN | 172.16.1.0/24 | LAN Interface |
| VMnet3 | DMZ | 10.0.0.0/24 | OPT1 Interface |
| NAT | WAN | 192.168.168.0/24 | WAN Interface |

---

## 📊 Luồng Dữ Liệu

```
┌─────────────┐    Syslog UDP      ┌─────────────────┐
│   pfSense   │ ──── Port 5514 ──► │                 │
│  +Suricata  │                    │  Splunk SIEM    │
└─────────────┘                    │  172.16.1.20    │
                                   │                 │
┌─────────────┐    TCP Port 9997   │  3 Index:       │
│  Windows 10 │ ──────────────────►│  win10eventlog  │
│  +Sysmon    │                    │  win10sysmon    │
│  +SUF       │                    │  win10powershell│
└─────────────┘                    └────────┬────────┘
                                            │
                                   Webhook HTTP POST
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │   n8n SOAR      │
                                   │   172.16.1.30   │
                                   └────────┬────────┘
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
                    ▼                       ▼                       ▼
           ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
           │  AbuseIPDB   │       │  VirusTotal  │       │   Gemini AI  │
           │  (IP check)  │       │ (Hash check) │       │ (PS analyze) │
           └──────┬───────┘       └──────┬───────┘       └──────┬───────┘
                  │                      │                       │
                  └──────────────────────┴───────────────────────┘
                                         │
                                  Gemini AI Analysis
                                         │
                                         ▼
                                ┌─────────────────┐
                                │  Telegram Bot   │
                                │  SOC Alert 🔴🟡🟢│
                                └─────────────────┘
```

### Thời Gian Phản Hồi Pipeline

| Giai Đoạn | Thời Gian |
|-----------|-----------|
| Splunk phát hiện (alert schedule) | ≤ 60 giây |
| n8n nhận Webhook | < 1 giây |
| Threat Intel API (AbuseIPDB / VT) | 2 – 5 giây |
| Gemini phân tích | 3 – 8 giây |
| Telegram gửi alert | < 1 giây |
| **Tổng thời gian** | **< 75 giây** |

---

## 👨‍💻 Tác Giả

<div align="center">

**Nguyễn Thanh Long**  
*Information Assurance Student — FPT University Hanoi*  
*Blue Team | SOC Analyst | Homelab Builder*

[![GitHub](https://img.shields.io/badge/GitHub-longnt05--afk-181717?style=for-the-badge&logo=github)](https://github.com/longnt05-afk)

</div>

---

<div align="center">

*Bài lab này được thực hiện như một phần trong quá trình tự học và xây dựng kỹ năng thực chiến hướng đến vị trí SOC Analyst.*

**⭐ Nếu bài lab này có ích, hãy để lại một star!**

</div>
