# Suricata Network Threat Intelligence & IDS/IPS Dashboard

## Mục đích (Purpose)
Dashboard này phục vụ công tác phân tích chuyên sâu các sự kiện an ninh mạng thu thập từ hệ thống giám sát và ngăn ngừa xâm nhập **Suricata IDS/IPS**. Dashboard giúp đội ngũ SOC theo dõi tổng quan các chỉ số vi phạm (Total Alerts, High Severity Alerts, Unique Signatures), phân tích các giao thức mạng phổ biến (DNS, HTTP, TLS) và nhanh chóng nhận diện các địa chỉ IP nguồn đang phát sinh hành vi độc hại.

---

## Nguồn dữ liệu (Data Source)
* **Index:** `suricata`
* **Sourcetype:** `suricata:json` / `eve:json`
* **Format:** Eve JSON log stream (sử dụng lệnh `spath` để trích xuất cấu trúc dữ liệu JSON)

---

## Bố trí và Chức năng các Panel (Panel Layout)

| Tên Panel | Kiểu hiển thị | Chức năng & Nghiệp vụ |
| :--- | :--- | :--- |
| **Total Suricata Events** | Single Value | Tổng số lượng bản ghi sự kiện (tất cả các loại event_type) thu thập từ Suricata. |
| **Alerts** | Single Value | Tổng số lượng cảnh báo an ninh (Alert) được kích hoạt. |
| **High Severity Alerts** | Single Value | Số lượng cảnh báo thuộc mức độ nghiêm trọng cao (Critical & High - Severity ≤ 2). |
| **Unique Signatures** | Single Value | Số lượng luật/chữ ký nhận dạng vi phạm (Rules/Signatures) độc lập đã bị kích hoạt. |
| **Unique Sources** | Single Value | Số lượng địa chỉ IP nguồn độc lập phát sinh lưu lượng hoặc cảnh báo. |
| **Suricata Timeline** | Line Chart | Xu hướng lưu lượng các sự kiện theo thời gian (chu kỳ 30 phút) phân loại theo event_type. |
| **Severity** | Pie Chart | Tỷ lệ phân bổ mức độ nghiêm trọng của cảnh báo (Critical, High, Medium, Low). |
| **Event Types** | Bar Chart | Thống kê phân bổ số lượng sự kiện theo từng loại giao thức/loại log (Alert, DNS, HTTP, TLS...). |
| **Top Signatures** | Bar Chart | Top 15 luật/chữ ký cảnh báo vi phạm bị kích hoạt thường xuyên nhất. |
| **Top Source IPs** | Bar Chart | Top 15 địa chỉ IP nguồn vi phạm/phát sinh nhiều cảnh báo nhất. |
| **Destination Ports** | Bar Chart | Top 15 Cổng đích (Destination Port) bị nhắm mục tiêu nhiều nhất trong các cảnh báo. |
| **DNS** | Table | Danh sách Top 40 tên miền (RRNAME) được truy vấn DNS nhiều nhất kèm IP nguồn. |
| **HTTP** | Table | Bảng 40 kết nối HTTP mới nhất chi tiết Hostname, URL và User-Agent. |
| **TLS** | Table | Bảng Top 40 kết nối mã hóa TLS chi tiết Server Name Indication (SNI) và IP nguồn/đích. |
| **Recent Alerts** | Table | Danh sách 50 cảnh báo vi phạm mới nhất chi tiết Severity, Signature, Category, IP & Port. |