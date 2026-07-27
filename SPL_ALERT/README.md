# Splunk Security Alerts

Thư mục này chứa các correlation search và scheduled alert đang được sử dụng trong **Super SOC/SOAR HomeLab**. Các alert lấy dữ liệu đầu vào từ **LimaCharlie EDR**, **pfSense**, **Suricata** và **Sysmon**, rồi thực hiện chuẩn hóa, làm giàu, đánh giá rủi ro và gom nhóm trước khi chuyển sang **DFIR-IRIS** để điều tra.

## Danh sách alert

### 1. SOC - LimaCharlie EDR High Confidence Detection
Phát hiện các alert endpoint có độ tin cậy cao từ LimaCharlie EDR trong `index=edr`. Alert này chuẩn hóa thông tin tiến trình, tài sản và nguồn phát hiện, đánh giá Risk Score, xác định primary detection rồi gom các detection liên quan thành một cảnh báo duy nhất.

**Nguồn dữ liệu:** LimaCharlie EDR (`index=edr`)

**Phạm vi giám sát:** Endpoint Detection & Response

### 2. SOC - pfSense Management Access Attempt
Phát hiện các nỗ lực truy cập hoặc kết nối đến giao diện quản trị pfSense (các cổng quản trị như 22, 80, 443, 8443) và tính rủi ro dựa trên trạng thái quản lý nguồn, hành động firewall và số lần xảy ra.

**Nguồn dữ liệu:** pfSense firewall logs

**Phạm vi giám sát:** Firewall Management Security

### 3. SOC - pfSense Repeated Firewall Blocks
Phát hiện một địa chỉ IP bị pfSense chặn lặp lại nhiều lần trong một khoảng thời gian, bao gồm các nguồn bị block nhiều lần hoặc truy cập nhiều cổng khác nhau. Alert này hỗ trợ xác định hoạt động dò quét, brute-force hoặc truy cập không hợp lệ.

**Nguồn dữ liệu:** pfSense filter logs

**Phạm vi giám sát:** Repeated Network Policy Violations

### 4. SOC - Suricata High Confidence Threat Alert
Phát hiện các sự kiện Suricata có độ tin cậy cao liên quan đến malware, exploit, C2 hoặc các signature threat intelligence. Alert ưu tiên các cảnh báo có giá trị điều tra cao và chỉ chuyển những sự kiện quan trọng sang DFIR-IRIS.

**Nguồn dữ liệu:** Suricata IDS/IPS alerts

**Phạm vi giám sát:** Network Threat Detection

### 5. SOC - Suricata IPS Blocked Scanner
Phát hiện hoạt động scan hoặc reconnaissance bị Suricata IPS chặn, bao gồm quét cổng và DoS/DoS-like traffic. Alert tổng hợp thông tin nguồn, đích, signature và trạng thái chặn để hỗ trợ điều tra mạng.

**Nguồn dữ liệu:** Suricata IDS/IPS alerts

**Phạm vi giám sát:** Port Scanning & Reconnaissance

### 6. SOC - Sysmon PowerShell EncodedCommand
Phát hiện tiến trình PowerShell có tham số mã hóa như `-EncodedCommand`, `-enc`, hoặc biến thể tương đương trong Sysmon Event ID 1. Alert này giúp phát hiện hành vi thực thi lệnh bị che giấu, tải payload hoặc C2 trên endpoint Windows.

**Nguồn dữ liệu:** Sysmon process creation logs

**Phạm vi giám sát:** Suspicious PowerShell Execution

## Quy trình alert

1. Thu thập dữ liệu từ nguồn bảo mật
2. Chạy correlation search trên Splunk
3. Chuẩn hóa, làm giàu và tính Risk Score
4. Deduplication / nhóm cảnh báo liên quan
5. Tạo Splunk alert
6. Chuyển tiếp cảnh báo sang webhook và DFIR-IRIS

## Định dạng file

Mỗi file `.yaml` chứa cấu hình alert Splunk, bao gồm:
- SPL search
- Lịch chạy và khoảng thời gian tìm kiếm
- Điều kiện kích hoạt cảnh báo
- Chuẩn hóa và làm giàu dữ liệu
- Risk Score và mức độ nghiêm trọng
- Cơ chế deduplication/gom nhóm cảnh báo
- Thông tin chuyển tiếp sang DFIR-IRIS

## Mục tiêu dự án

Các alert được thiết kế cho môi trường **Super SOC/SOAR HomeLab** với mục tiêu:
- Chỉ chuyển cảnh báo có giá trị điều tra cao
- Giảm thiểu noise và cảnh báo trùng lặp
- Cung cấp đủ context cho SOC Analyst
- Hỗ trợ quy trình triage, investigation và incident response trên DFIR-IRIS
