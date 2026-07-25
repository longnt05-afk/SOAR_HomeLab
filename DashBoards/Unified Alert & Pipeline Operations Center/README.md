# SuperSOAR SOC - Unified Alert Operations Dashboard

## Mục đích (Purpose)

Dashboard này phục vụ công tác giám sát, phân loại (triage) và theo dõi toàn bộ các cảnh báo an ninh (SOC Alert Instances) được phát sinh từ hệ thống Splunk. Dashboard cho phép đội ngũ vận hành SOC nắm bắt nhanh số lượng cảnh báo theo mức độ nghiêm trọng (Severity), nguồn phát sinh (LimaCharlie EDR, Suricata, Windows, pfSense...), theo dõi luồng cảnh báo theo thời gian thực và kiểm tra trạng thái tích hợp tự động hóa qua IRIS SOAR Webhook.

---

## Nguồn dữ liệu (Data Source)

- **API / Endpoint:** Splunk REST API (`/servicesNS/-/-/alerts/fired_alerts/-`)
- **Saved Searches Filter:** `SOC - *`
- **Integrations:** DFIR-IRIS / Webhook integration flags

---

## Bố trí và Chức năng các Panel (Panel Layout)

| Tên Panel                              | Kiểu hiển thị   | Chức năng & Nghiệp vụ                                                                                                        |
| :------------------------------------- | :-------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Tracked Alert Instances**            | Single Value    | Tổng số lượt cảnh báo SOC đã bị kích hoạt trong khoảng thời gian chọn.                                                       |
| **High / Critical**                    | Single Value    | Số lượng cảnh báo thuộc mức độ nghiêm trọng High hoặc Critical.                                                              |
| **Triggered SOC Rules**                | Single Value    | Số lượng quy tắc/luật cảnh báo độc lập (Unique Rules) đã bị kích hoạt.                                                       |
| **IRIS-Bound Triggers**                | Single Value    | Số lượng cảnh báo đã được đẩy tự động sang hệ thống IRIS SOAR qua Webhook.                                                   |
| **Ready SOC Alerts**                   | Single Value    | Số lượng quy tắc cảnh báo đã được cấu hình hoàn chỉnh và sẵn sàng hoạt động.                                                 |
| **Tracked Alert Timeline by Severity** | Line/Area Chart | Biểu đồ chuỗi thời gian biến động cảnh báo (span 30m) phân loại theo Severity.                                               |
| **Severity Distribution**              | Pie Chart       | Tỷ lệ phần trăm phân bổ cảnh báo theo mức độ nghiêm trọng (Critical, High, Medium, Low, Info).                               |
| **Alert Source Distribution**          | Pie Chart       | Tỷ lệ cảnh báo phân bổ theo từng nguồn dữ liệu (LimaCharlie, Suricata, Windows, pfSense...).                                 |
| **Triggers by SOC Alert**              | Bar Chart       | Top 10 quy tắc cảnh báo bị kích hoạt nhiều nhất trong hệ thống.                                                              |
| **Operational Alert Queue**            | Table           | Hàng chờ cảnh báo thực thi chi tiết mốc thời gian, Severity, Rule Name, Source, IRIS Bound, Search SID và thời gian hết hạn. |
| **Alert Trigger Summary**              | Table           | Bảng tổng hợp theo từng Rule bao gồm tổng số lần kích hoạt, mốc kích hoạt mới nhất và trạng thái liên kết IRIS.              |

# SuperSOAR SOC - Correlation & Pipeline Health Dashboard

## Mục đích (Purpose)

Dashboard này phục vụ công tác quản trị kỹ thuật, kiểm tra sức khỏe hệ thống thu thập dữ liệu (Data Ingestion Pipeline) và phân tích tương quan nâng cao. Dashboard giúp kỹ sư SOC giám sát độ tươi của dữ liệu (Data Freshness), phát hiện các nguồn log bị gián đoạn (Stale/Missing), kiểm tra trạng thái lập lịch chạy cảnh báo (Scheduler Execution Health), đánh giá mức độ sẵn sàng của các trường dữ liệu phục vụ tương quan (Correlation Field Readiness) và thực hiện tương quan đa nguồn theo thời gian thực (5-Tuple, Endpoint Process, DNS Overlap).

---

## Nguồn dữ liệu (Data Source)

- **Internal Logs:** `_internal` (sourcetype=scheduler)
- **REST API:** Splunk Saved Searches Configuration (`/servicesNS/-/-/saved/searches`)
- **Data Indexes:** `edr`, `pfsense`, `suricata`, `win10sysmon`, `win10powershell`, `win10eventlog`

---

## Bố trí và Chức năng các Panel (Panel Layout)

| Tên Panel                                  | Kiểu hiển thị | Chức năng & Nghiệp vụ                                                                                                   |
| :----------------------------------------- | :------------ | :---------------------------------------------------------------------------------------------------------------------- |
| **Healthy Data Sources**                   | Single Value  | Số lượng nguồn dữ liệu đang đẩy log ổn định (độ trễ ≤ 15 phút).                                                         |
| **Delayed / Stale / Missing**              | Single Value  | Số lượng nguồn dữ liệu đang gặp sự cố gián đoạn hoặc trễ log.                                                           |
| **Configured SOC Alerts**                  | Single Value  | Tổng số lượng quy tắc cảnh báo SOC đã được khởi tạo trong hệ thống.                                                     |
| **Webhook-Configured Alerts**              | Single Value  | Số lượng Rule đã cấu hình Webhook để gửi tin nhắn/cảnh báo ra bên ngoài.                                                |
| **Scheduler Issues**                       | Single Value  | Tổng số lượt chạy bị bỏ qua (Skipped) hoặc lỗi (Failed) của bộ lập lịch Splunk Scheduler.                               |
| **Expected Data Source Freshness**         | Table         | Theo dõi độ trễ (Age in Minutes), thời điểm nhận log cuối và tổng số event của từng Index.                              |
| **SOC Alert Configuration Validation**     | Table         | Kiểm tra tính hợp lệ cấu hình từng Rule (Trạng thái Enable, Schedule, Webhook, Cron, Earliest/Latest).                  |
| **Saved Alert Scheduler Execution Health** | Table         | Giám sát lịch sử thực thi của Scheduler (Trạng thái chạy gần nhất, trung bình thời gian xử lý, số lượt Skipped/Failed). |
| **pfSense + Suricata 5-Tuple Correlation** | Table         | Tương quan kết nối mạng trùng khớp đồng thời 5 chỉ số (5-Tuple) giữa Firewall và IDS trong cửa sổ 5 phút.               |
| **LimaCharlie + PowerShell Correlation**   | Table         | Tương quan hành vi nghi vấn trên Endpoint giữa EDR LimaCharlie và PowerShell Log 4104 trong cửa sổ 5 phút.              |
| **Suricata + Sysmon DNS Correlation**      | Table         | Tương quan truy vấn tên miền trùng khớp giữa Suricata DNS và Sysmon EventID 22 trong cửa sổ 5 phút.                     |
| **Correlation Field Readiness**            | Table         | Đánh giá phần trăm dữ liệu đáp ứng đầy đủ các trường thông tin bắt buộc để thực hiện tương quan.                        |
| **Event Volume**                           | Bar Chart     | Thống kê tổng số lượng log phát sinh phân theo từng Index trong khoảng thời gian phân tích.                             |
