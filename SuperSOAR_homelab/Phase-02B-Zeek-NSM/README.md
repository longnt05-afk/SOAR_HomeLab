\# Phase 2 – Tích hợp Zeek Network Security Monitoring (NSM)





\## Mục tiêu



\- Triển khai Zeek làm cảm biến Network Security Monitoring (NSM).

\- Thu thập metadata của lưu lượng mạng nội bộ.

\- Chuyển tiếp log Zeek về Splunk Enterprise.

\- Xây dựng index riêng (`index=zeek`) để quản lý dữ liệu.

\- Thiết kế Dashboard giám sát Zeek trên Splunk.

\- Chuẩn bị dữ liệu phục vụ Correlation Search và các giai đoạn SOAR tiếp theo.



\---



\## Kết quả đạt được



\- Hoàn thành triển khai Zeek trên Ubuntu Server.

\- Thu thập thành công các log:

&#x20; - `conn.log`

&#x20; - `dns.log`

&#x20; - `http.log`

&#x20; - `ssl.log`

&#x20; - `files.log`

&#x20; - `notice.log`

\- Forward toàn bộ log về Splunk thông qua Splunk Universal Forwarder.

\- Xây dựng Dashboard Zeek NSM giúp theo dõi:

&#x20; - Tổng số sự kiện Zeek

&#x20; - Timeline kết nối mạng

&#x20; - DNS Queries

&#x20; - HTTP Requests

&#x20; - TLS/SSL Activity

&#x20; - Top External Destinations

\- Bổ sung khả năng giám sát mạng chuyên sâu cho hệ thống SOC Lab.



\---



