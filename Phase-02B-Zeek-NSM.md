# 📡 Báo cáo: Tích hợp Zeek NSM vào SuperSOAR HomeLab

---

## 1. Network Security Monitoring (NSM) là gì?

**Network Security Monitoring (NSM)** là phương pháp luận thu thập, phát hiện và phân tích các dấu hiệu xâm nhập trên hạ tầng mạng theo thời gian thực. Khác với Firewall hay IDS/IPS — vốn chỉ tập trung vào việc **chặn** hoặc **cảnh báo** dựa trên signature đã biết — NSM tiếp cận theo hướng **visibility-first**: ghi nhận toàn bộ metadata lưu lượng mạng để phục vụ cho việc phân tích sâu, threat hunting và điều tra sự cố (incident response).

Một hệ thống NSM hoàn chỉnh thường bao gồm:

- **Sensor**: Thiết bị hoặc phần mềm đặt tại các điểm chiến lược trong mạng để capture traffic.
- **Log & Metadata Engine**: Bóc tách và cấu trúc hóa dữ liệu từ các giao thức mạng (DNS, HTTP, TLS, ...).
- **SIEM / Analytics Platform**: Nơi tập trung, tương quan và trực quan hóa dữ liệu (trong dự án này là Splunk).

> NSM không thay thế Firewall hay IDS, mà **bổ sung một lớp visibility** mà các công cụ truyền thống không cung cấp được — đặc biệt hữu ích khi kẻ tấn công đã bypass được các lớp phòng thủ vòng ngoài.

---

## 2. Zeek là gì?

**Zeek** (trước đây gọi là **Bro**) là một nền tảng phân tích lưu lượng mạng mã nguồn mở, được phát triển từ năm 1994 bởi **Vern Paxson** tại UC Berkeley. Zeek hoạt động như một **passive network sensor** — lắng nghe traffic mà không can thiệp vào luồng dữ liệu.

Điểm mạnh cốt lõi của Zeek:

| Đặc điểm | Mô tả |
| :--- | :--- |
| **Protocol Analysis** | Tự động bóc tách metadata từ hàng chục giao thức: DNS, HTTP, SSL/TLS, SMB, FTP, SSH, ... |
| **Structured Logging** | Xuất log dưới dạng có cấu trúc (JSON/TSV), dễ dàng ingest vào SIEM. |
| **Scripting Engine** | Ngôn ngữ scripting riêng cho phép tùy biến detection logic và policy. |
| **File Extraction** | Có khả năng trích xuất file truyền qua mạng để phân tích malware. |
| **Community & Ecosystem** | Được sử dụng rộng rãi trong các SOC, CERT và tổ chức nghiên cứu bảo mật toàn cầu. |

> Zeek **không phải là IDS** theo nghĩa truyền thống — nó không chặn hay alert dựa trên signature đơn thuần. Thay vào đó, Zeek tạo ra một **bức tranh toàn cảnh** về mọi hoạt động mạng, cho phép analyst phát hiện các hành vi bất thường mà signature-based detection bỏ sót.

---

## 3. Tại sao chọn Zeek cho SuperSOAR HomeLab?

Trong kiến trúc SuperSOAR HomeLab hiện tại, hệ thống đã có:

- **pfSense** → Firewall log (allow/deny traffic).
- **Suricata** → IDS alert dựa trên signature.
- **Sysmon** → Endpoint telemetry (process, network connection, file).

Tuy nhiên, vẫn tồn tại một **khoảng trống visibility** quan trọng:

| Câu hỏi cần trả lời | pfSense | Suricata | Sysmon | **Zeek** |
| :--- | :---: | :---: | :---: | :---: |
| Host nào query domain nào qua DNS? | ❌ | ⚠️ | ❌ | ✅ |
| Chi tiết HTTP request (URI, User-Agent, Host)? | ❌ | ⚠️ | ❌ | ✅ |
| TLS certificate & SNI metadata? | ❌ | ⚠️ | ❌ | ✅ |
| File hash của file truyền qua mạng? | ❌ | ❌ | ❌ | ✅ |
| Toàn bộ connection metadata (bytes, duration, state)? | ⚠️ | ❌ | ⚠️ | ✅ |

> ✅ = Đầy đủ &nbsp;&nbsp; ⚠️ = Hạn chế &nbsp;&nbsp; ❌ = Không hỗ trợ

**Zeek lấp đầy khoảng trống đó** bằng cách cung cấp **network metadata ở mức giao thức** — thứ mà không công cụ nào khác trong lab có thể cung cấp. Việc tích hợp Zeek giúp SuperSOAR HomeLab đạt được mô hình **SOC visibility đa tầng** hoàn chỉnh, sẵn sàng cho các use case correlation và SOAR automation ở các phase tiếp theo.

---

## 4. Tổng quan dự án

Dự án này mở rộng kiến trúc **SuperSOAR HomeLab** bằng cách bổ sung giải pháp **Zeek Network Security Monitoring (NSM)** làm một nguồn thu thập network telemetry độc lập. Zeek được triển khai dưới dạng một **network sensor** nhằm mục đích capture và trích xuất các metadata có cấu trúc từ lưu lượng mạng nội bộ. Dữ liệu này sau đó được forward trực tiếp về **Splunk Enterprise** để tiến hành phân tích và trực quan hóa.

Mục tiêu cốt lõi của giai đoạn này là gia tăng khả năng hiển thị mạng vượt ra khỏi giới hạn của các cảnh báo Firewall hay IDS truyền thống. Quá trình này tập trung vào việc thu thập metadata ở tầng giao thức, bao gồm thông tin chi tiết về các connection, truy vấn DNS, request HTTP, phiên TLS/SSL, tệp tin và các notice từ hệ thống.

---

## 5. Mục tiêu triển khai

- Triển khai Zeek đóng vai trò là một **NSM sensor** chuyên dụng.
- Thu thập network metadata từ traffic của hệ thống lab.
- Thiết lập quá trình forward log từ Zeek đến Splunk Enterprise.
- Khởi tạo không gian lưu trữ độc lập trên Splunk qua `index=zeek`.
- Xây dựng **Zeek NSM Dashboard** phục vụ giám sát tập trung.
- Chuẩn bị nền tảng dữ liệu Zeek để thực hiện correlation với pfSense, Suricata, Sysmon và các workflow của SOAR trong tương lai.

---

## 6. Kiến trúc mạng

```
Windows 10 Victim / Kali / pfSense LAN
            ↓
     Ubuntu Zeek Sensor
            ↓
       Zeek Log Files
            ↓
  Splunk Universal Forwarder
            ↓
     Splunk Enterprise
            ↓
       index=zeek
            ↓
Zeek NSM Dashboard / Correlation Search
```

### Data Flow

```
Network Traffic ──▶ Zeek Sensor ──▶ conn.log / dns.log / http.log / ssl.log / files.log / notice.log
       ──▶ Splunk Universal Forwarder ──▶ Splunk index=zeek ──▶ Zeek NSM Dashboard
```

---

## 7. Các thành phần hệ thống

![Sơ đồ hệ thống](Phase-02B-Zeek-NSM_images/img_007_8bfd0f78.png)

---

## 8. Danh mục Zeek Log thu thập

Quá trình tích hợp đã đẩy thành công các loại log đặc thù sau của Zeek vào Splunk:

| Sourcetype    | Cấu trúc dữ liệu ghi nhận                                      |
| :------------ | :--------------------------------------------------------------- |
| `zeek:conn`   | Metadata của các network connection (TCP/UDP/ICMP...).           |
| `zeek:dns`    | Các truy vấn DNS và thông tin response tương ứng.                |
| `zeek:http`   | Chi tiết các request và response qua giao thức HTTP.             |
| `zeek:ssl`    | Thông tin bắt tay mã hóa và metadata của phiên TLS/SSL.         |
| `zeek:files`  | Metadata của các tệp tin được truyền tải qua mạng.              |
| `zeek:notice` | Các alert được kích hoạt dựa trên script policy của Zeek.        |

### Xác thực trên Splunk

![Xác thực Sourcetype trên Splunk](Phase-02B-Zeek-NSM_images/img_005_37dfd525.png)

> **Kết quả:** Hệ thống ghi nhận đầy đủ các sourcetype định tuyến vào Splunk bao gồm: `zeek:conn`, `zeek:dns`, `zeek:http`, `zeek:ssl`, `zeek:files` và `zeek:notice`.

---

## 9. Triển khai Zeek NSM Sensor

### 9.1. Cài đặt Zeek

Thêm repository và cài đặt Zeek trên Ubuntu:

```bash
echo 'deb https://download.opensuse.org/repositories/security:/zeek/xUbuntu_24.04/ /' \
  | sudo tee /etc/apt/sources.list.d/security:zeek.list

curl -fsSL https://download.opensuse.org/repositories/security:zeek/xUbuntu_24.04/Release.key \
  | gpg --dearmor \
  | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null

sudo apt install zeek-8.0 -y
```

![Cài đặt Zeek](Phase-02B-Zeek-NSM_images/img_003_7ef2ae86.png)

### 9.2. Cấu hình card mạng

Cấu hình 2 card mạng: 1 card để tải các gói và 1 card `ens34` dùng để thêm vào vùng LAN.

![Cấu hình card mạng](Phase-02B-Zeek-NSM_images/img_001_8e59cfe1.png)

### 9.3. Cấu hình Zeek Sensor

Sửa interface thành card LAN:

```bash
sudo nano /opt/zeek/etc/node.cfg
```

![Cấu hình node.cfg](Phase-02B-Zeek-NSM_images/img_009_5e10b54e.png)

Thêm Zeek vào `PATH`:

```bash
echo 'export PATH=/opt/zeek/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

Bật JSON log cho Zeek — thêm dòng sau vào cuối file `local.zeek`:

```bash
sudo nano /opt/zeek/share/zeek/site/local.zeek
# Thêm dòng sau vào cuối file:
# @load policy/tuning/json-logs.zeek
```

![Bật JSON log](Phase-02B-Zeek-NSM_images/img_008_013525fe.png)

### 9.4. Deploy Zeek

```bash
sudo /opt/zeek/bin/zeekctl check
sudo /opt/zeek/bin/zeekctl deploy
sudo /opt/zeek/bin/zeekctl status
```

![Zeek deploy status](Phase-02B-Zeek-NSM_images/img_006_85662615.png)

### 9.5. Cấu hình Splunk Universal Forwarder

Tạo `index=zeek` mới trên Splunk Web UI, sau đó cài đặt và cấu hình Splunk Universal Forwarder trên Ubuntu Zeek:

```bash
sudo /opt/splunkforwarder/bin/splunk start --accept-license
sudo /opt/splunkforwarder/bin/splunk enable boot-start -systemd-managed 1
sudo /opt/splunkforwarder/bin/splunk add forward-server 172.16.1.20:9997
```

![Test kết nối Forwarder](Phase-02B-Zeek-NSM_images/img_004_8969521b.png)

### 9.6. Tạo inputs cho Zeek Logs

```bash
sudo mkdir -p /opt/splunkforwarder/etc/apps/zeek_inputs/local
sudo nano /opt/splunkforwarder/etc/apps/zeek_inputs/local/inputs.conf
```

![Cấu hình inputs.conf](Phase-02B-Zeek-NSM_images/img_002_0e08b2aa.png)

### 9.7. Xác nhận log đã được đẩy lên Splunk

![Log trên Splunk](Phase-02B-Zeek-NSM_images/img_005_37dfd525.png)

---

## 10. Zeek NSM Dashboard

Giao diện trực quan hóa dữ liệu **Zeek NSM Overview - SuperSOAR** build hoàn chỉnh trên Splunk, tập trung vào các panel giám sát sau:

### Total Zeek Events

```spl
index=zeek earliest=$time.earliest$ latest=$time.latest$
| stats count
```

### Zeek Log Types

```spl
index=zeek earliest=$time.earliest$ latest=$time.latest$
| stats count by sourcetype
| sort - count
```

### Connection Timeline

```spl
index=zeek sourcetype=zeek:conn earliest=$time.earliest$ latest=$time.latest$
| timechart span=30m count
```

### Top External Destinations

```spl
index=zeek sourcetype=zeek:conn earliest=$time.earliest$ latest=$time.latest$
| spath
| eval src=coalesce('id.orig_h',src_ip), dest=coalesce('id.resp_h',dest_ip), dest_port=coalesce('id.resp_p',dest_port), proto=coalesce(proto,proto)
| stats count sum(orig_bytes) as orig_bytes sum(resp_bytes) as resp_bytes by src dest dest_port proto
| sort - count
| head 20
```

### DNS Queries

```spl
index=zeek sourcetype=zeek:dns earliest=$time.earliest$ latest=$time.latest$
| spath
| eval src=coalesce('id.orig_h',src_ip), query=coalesce(query,'dns.rrname')
| stats count dc(src) as unique_clients by query
| sort - count
| head 25
```

### HTTP Requests

```spl
index=zeek sourcetype=zeek:http earliest=$time.earliest$ latest=$time.latest$
| spath
| eval src=coalesce('id.orig_h',src_ip), dest=coalesce('id.resp_h',dest_ip)
| table _time src dest host uri method user_agent status_code
| sort - _time
| head 50
```

![Zeek NSM Dashboard](Phase-02B-Zeek-NSM_images/img_010_c53464e2.png)

---

## 11. Đánh giá khả năng hiển thị

Sau khi deploy, sensor đã thu thập và bóc tách thành công các luồng traffic tiêu biểu:

### 🔍 Khả năng giám sát DNS

Ghi nhận rõ ràng các truy vấn phân giải tên miền từ nội bộ, ví dụ: `ntp.ubuntu.com`, `quickdraw.splunk.com`, `apps.splunk.com`. Giúp nhanh chóng audit các domain lạ.

### 🌐 Khả năng giám sát HTTP

Log `zeek:http` cung cấp toàn bộ metadata của các phiên HTTP cleartext bao gồm URI, host, và user-agent, hỗ trợ phát hiện các request tải payload bất thường.

### 🔗 Khả năng giám sát Connection

Đặc tả chi tiết các luồng giao tiếp với IP nguồn, IP đích, port, giao thức, dung lượng truyền tải và connection state. Trực tiếp phục vụ cho việc detect hành vi scan mạng hoặc C2 beaconing.

---

## 12. Các Use Case phân tích bảo mật

Dữ liệu từ Zeek cung cấp input chất lượng để xây dựng các SOC Use Case sau:

| Tên Use Case                                  | Nguồn Log Zeek phụ thuộc  |
| :--------------------------------------------- | :------------------------- |
| Truy vấn phân giải các malicious domain        | `zeek:dns`                 |
| Tải payload từ các host độc hại qua web        | `zeek:http`, `zeek:files`  |
| Hành vi Port Scanning nội bộ                   | `zeek:conn`                |
| Luồng outbound traffic bất thường              | `zeek:conn`                |
| Header TLS SNI sai lệch hoặc đáng ngờ         | `zeek:ssl`                 |
| Truyền file nghi ngờ qua HTTP                  | `zeek:http`, `zeek:files`  |
| Bất thường kích hoạt từ policy Zeek            | `zeek:notice`              |

---

## 13. Tổng kết

Giai đoạn nâng cấp này đã tích hợp hoàn hảo **Zeek** vào kiến trúc **SuperSOAR HomeLab** với vai trò là một NSM sensor chuyên dụng. Các luồng metadata mạng có cấu trúc đang được đẩy ổn định vào `index=zeek`, mở ra khả năng visibility sâu rộng đối với các activity của DNS, HTTP, TLS, file transfer và connection.

Hệ thống lab hiện tại đã đảm bảo năng lực **SOC coverage** trên 3 vector chủ chốt:

| Vector                          | Nguồn dữ liệu                         |
| :------------------------------ | :------------------------------------- |
| **Endpoint Telemetry**          | Windows Event Log, Sysmon, PowerShell  |
| **Security Device Telemetry**   | pfSense, Suricata                      |
| **Network Telemetry**           | Zeek                                   |

> 

---
