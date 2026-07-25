# pfSense Firewall Traffic & Security Analysis Dashboard

## Mục đích (Purpose)

Dashboard này được xây dựng nhằm giám sát toàn bộ lưu lượng mạng và phân tích sự kiện an ninh từ hệ thống tường lửa **pfSense Firewall**. Dashboard hỗ trợ đội ngũ SOC/Network Security theo dõi tổng quan số lượng truy cập, phân loại các hành động chặn (Block/Deny) vs cho phép (Pass/Allow), nhận diện các IP nguồn/đích phát sinh lưu lượng lớn và tự động cảnh báo các địa chỉ IP có hành vi tấn công dò quét lặp đi lặp lại.

---

## Nguồn dữ liệu (Data Source)

- **Index:** `pfsense`
- **Sourcetype:** `pfsense:filterlog` / `syslog`
- **Format:** Syslog Raw text (trích xuất thông tin IP và Action bằng regex/eval)

---

## Bố trí và Chức năng các Panel (Panel Layout)

| Tên Panel                   | Kiểu hiển thị | Chức năng & Nghiệp vụ                                                            |
| :-------------------------- | :------------ | :------------------------------------------------------------------------------- |
| **Total Firewall Events**   | Single Value  | Tổng số lượng sự kiện/log tường lửa đã thu thập được.                            |
| **Block Count**             | Single Value  | Tổng số lượt kết nối bị tường lửa ngăn chặn (Block/Deny).                        |
| **Pass Count**              | Single Value  | Tổng số lượt kết nối được phép đi qua tường lửa (Pass/Allow).                    |
| **Unique Sources**          | Single Value  | Số lượng địa chỉ IP nguồn độc lập khởi tạo lưu lượng.                            |
| **Repeated Blockers Count** | Single Value  | Số lượng IP nguồn bị chặn lặp lại từ 20 lần trở lên (nghi vấn dò quét/tấn công). |
| **Firewall Timeline**       | Line Chart    | Xu hướng lưu lượng mạng (Pass vs Block) mỗi 30 phút theo thời gian.              |
| **Action Breakdown**        | Pie Chart     | Tỷ lệ phần trăm phân bổ giữa các hành động Block, Pass và Unknown.               |
| **Top Sources**             | Bar Chart     | Top 15 địa chỉ IP nguồn phát sinh lưu lượng lớn nhất.                            |
| **Top Destinations**        | Bar Chart     | Top 15 địa chỉ IP đích nhận nhiều lưu lượng nhất.                                |
| **Repeated Blockers**       | Table         | Danh sách các IP bị chặn nhiều lần kèm số lượt, IP đích và mốc thời gian.        |
| **Source Health**           | Table         | Giám sát trạng thái đẩy log của từng Host/Source/Sourcetype.                     |
| **Recent Firewall Events**  | Table         | Bảng 60 sự kiện lưu lượng mới nhất chi tiết IP nguồn, IP đích và raw log.        |
