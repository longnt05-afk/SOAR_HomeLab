# Security Operations Center (SOC) Executive Dashboard

## Mục đích (Purpose)

Dashboard này đóng vai trò là trung tâm điều hành tổng quan (Executive Overview) cho toàn bộ hệ thống SOC. Dashboard tổng hợp dữ liệu thời gian thực từ nhiều tầng phòng thủ khác nhau bao gồm Tường lửa (pfSense), Hệ thống phát hiện xâm nhập (Suricata IDS), Giải pháp giám sát điểm cuối (LimaCharlie EDR) và Nhật ký hệ thống Windows (Security Event Log, Sysmon, PowerShell).

Thông qua các chỉ số đo lường trung tâm, biểu đồ xu hướng và các thuật toán tương quan đa nguồn (Cross-source Correlation), phân tích viên SOC có thể nhanh chóng nắm bắt diện mạo an ninh hệ thống, phát hiện các mối đe dọa có tính chất phức tạp và ưu tiên xử lý các sự kiện nguy cơ cao.

---

## Nguồn dữ liệu (Data Source)

- **Macro tổng hợp:** `soc_indexes`
- **Indexes tích hợp:** `pfsense`, `suricata`, `win10eventlog`, `win10sysmon`, `win10powershell`, `edr`
- **Sourcetypes:** `pfsense:filterlog`, `suricata:json`, `limacharlie:json`, `XmlWinEventLog:Security`, `XmlWinEventLog:Microsoft-Windows-Sysmon/Operational`, `XmlWinEventLog:Microsoft-Windows-PowerShell/Operational`

---

## Bố trí và Chức năng các Panel (Panel Layout)

| Tên Panel                     | Kiểu hiển thị | Chức năng & Nghiệp vụ                                                                                  |
| :---------------------------- | :------------ | :----------------------------------------------------------------------------------------------------- |
| **Total SOC Events**          | Single Value  | Tổng số lượng sự kiện/bản ghi log đã thu thập được trên toàn bộ hệ thống.                              |
| **Active Hosts**              | Single Value  | Số lượng máy trạm và máy chủ độc lập đang hoạt động và gửi log về SOC.                                 |
| **Suricata Alerts**           | Single Value  | Tổng số lượng cảnh báo xâm nhập mạng được ghi nhận từ Suricata IDS.                                    |
| **Windows High Value Events** | Single Value  | Số lượng sự kiện an ninh nguy cơ cao từ các máy chủ/máy trạm Windows.                                  |
| **Correlated IPs**            | Single Value  | Số lượng địa chỉ IP nghi vấn xuất hiện đồng thời trên nhiều nguồn log (Tường lửa + IDS).               |
| **SOC Timeline**              | Line Chart    | Biểu đồ chuỗi thời gian theo dõi biến động số lượng log mỗi 30 phút phân theo từng Index.              |
| **Signal Mix**                | Pie Chart     | Tỷ lệ phân bổ dữ liệu theo miền nghiệp vụ (Windows Security, Sysmon, PowerShell, Firewall, IDS/IPS).   |
| **Data Sources**              | Bar Chart     | Thống kê và xếp hạng tổng số lượng log thu thập được phân theo từng Index nguồn.                       |
| **Top Hosts**                 | Bar Chart     | Top 10 thiết bị/máy chủ phát sinh số lượng log lớn nhất trong hệ thống.                                |
| **Top Suricata Signatures**   | Bar Chart     | Top 10 luật/chữ ký cảnh báo vi phạm Suricata bị kích hoạt với tần suất cao nhất.                       |
| **Windows Event Codes**       | Bar Chart     | Thống kê tần suất xuất hiện của các mã Event ID quan trọng (4625, 1102, 4672, 4720...).                |
| **Priority Correlations**     | Table         | Danh sách các IP xuất hiện trên cả pfSense & Suricata kèm mốc thời gian phát hiện và tần suất vi phạm. |
| **Recent Notables**           | Table         | Bảng tổng hợp 50 cảnh báo đáng chú ý mới nhất từ Suricata, Windows và pfSense kèm phân mức Severity.   |
