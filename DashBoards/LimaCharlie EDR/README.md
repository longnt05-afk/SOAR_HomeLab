# LimaCharlie EDR Detection & Incident Response Dashboard

## Mục đích (Purpose)

Dashboard này được thiết kế nhằm theo dõi, giám sát và phân tích các mối đe dọa an ninh trên Endpoint được ghi nhận bởi hệ thống **LimaCharlie EDR**. Dashboard cung cấp góc nhìn toàn diện từ tổng quan chỉ số (Detections, Critical Alerts, Impacted Endpoints) cho đến chi tiết các hành vi nghi vấn (Suspicious Processes, Command Line execution) và định ánh xạ sang khung **MITRE ATT&CK**.

---

## Nguồn dữ liệu (Data Source)

- **Index:** `edr`
- **Sourcetype:** `limacharlie:json`
- **Format:** JSON Log Stream (truy vấn trường dữ liệu thông qua lệnh `spath`)

---

## Bố trí và Chức năng các Panel (Panel Layout)

| Tên Panel                 | Kiểu hiển thị | Chức năng & Nghiệp vụ                                                             |
| :------------------------ | :------------ | :-------------------------------------------------------------------------------- |
| **Total Detections**      | Single Value  | Tổng số lượng mối đe dọa/phát hiện EDR ghi nhận được.                             |
| **Critical Alerts**       | Single Value  | Số lượng cảnh báo mức nguy hiểm cao (Critical/High/Priority ≥ 3).                 |
| **Unique Endpoints**      | Single Value  | Số lượng thiết bị độc lập (Workstation/Server) bị ảnh hưởng.                      |
| **Active Rules**          | Single Value  | Số lượng Rule cảnh báo EDR đã bị kích hoạt.                                       |
| **MITRE Count**           | Single Value  | Số lượng kỹ thuật tấn công độc lập theo khung MITRE ATT&CK.                       |
| **Detection Timeline**    | Line Chart    | Xu hướng mối đe dọa theo thời gian (mỗi 1 giờ) phân loại theo Category.           |
| **Severity Distribution** | Pie Chart     | Tỷ lệ phân bổ mức độ nghiêm trọng (Critical, High, Medium, Low, Info).            |
| **Top Categories**        | Bar Chart     | Top 10 danh mục hành vi độc hại xuất hiện nhiều nhất.                             |
| **MITRE Techniques**      | Bar Chart     | Top 10 kỹ thuật MITRE ATT&CK bị vi phạm thường xuyên nhất.                        |
| **Suspicious Processes**  | Table         | Danh sách các tiến trình nghi vấn kèm Command Line, Parent Process, PID & Hash.   |
| **Recent Detections**     | Table         | Bảng 50 phát hiện mới nhất chi tiết thông tin Endpoint, IP, Severity và MITRE ID. |
