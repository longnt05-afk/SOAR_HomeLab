# pfSense & Suricata Network Performance and Threat Monitoring Dashboard

## Mục đích (Purpose)

Dashboard này phục vụ công tác giám sát hiệu năng phần cứng, lưu lượng mạng và các mối đe doạ trên hệ thống tường lửa **pfSense** kết hợp dữ liệu từ **Suricata IDS/IPS** và chỉ số **SNMP Metrics**. Dashboard cho phép đội ngũ SOC/Network Admin theo dõi sức khỏe phần cứng (CPU, Memory, State Table), băng thông mạng WAN (Mbps, PPS), độ trễ đường truyền Gateway (Latency/Loss), đồng thời phát hiện sớm các hành vi quét cổng hoặc tấn công từ chối dịch vụ (DoS/Scan Port).

---

## Nguồn dữ liệu (Data Source)

- **Index:** `pfsense`, `pfsense_snmp`, `suricata`
- **Sourcetype:** `pfsense:snmp:metric`, `syslog`, `suricata:json`
- **Metrics:** CPU usage, Memory usage, State Table usage, WAN In/Out BPS, WAN In/Out PPS, Gateway Loss/Latency

---

## Bố trí và Chức năng các Panel (Panel Layout)

| Tên Panel                 | Kiểu hiển thị | Chức năng & Nghiệp vụ                                                             |
| :------------------------ | :------------ | :-------------------------------------------------------------------------------- |
| **Blocks Latest**         | Single Value  | Tốc độ kết nối bị ngăn chặn (Block/Deny) trong phút gần nhất.                     |
| **CPU Latest**            | Single Value  | Phần trăm sử dụng CPU hiện tại của thiết bị Firewall.                             |
| **Memory Latest**         | Single Value  | Phần trăm sử dụng bộ nhớ RAM hiện tại của thiết bị Firewall.                      |
| **State Latest**          | Single Value  | Tỷ lệ chiếm dụng bảng trạng thái kết nối (State Table Usage %).                   |
| **WAN In Latest**         | Single Value  | Băng thông chiều vào (Inbound Traffic) mới nhất của cổng WAN (Mbps).              |
| **Firewall Blocks**       | Line Chart    | Xu hướng biến động số lượng kết nối bị chặn theo từng phút.                       |
| **Health Timeline**       | Line Chart    | Biểu đồ theo dõi song song các chỉ số sức khỏe hệ thống (CPU, RAM, State Table).  |
| **WAN BPS**               | Line Chart    | Biểu đồ lưu lượng băng thông WAN In/Out theo Mbps.                                |
| **WAN PPS**               | Line Chart    | Biểu đồ tổng số lượng gói tin xử lý trên giây (Packets Per Second) cổng WAN.      |
| **Gateway Loss Latency**  | Line Chart    | Theo dõi độ trễ (Latency - ms) và tỷ lệ mất gói (Loss - %) của Gateway.           |
| **Suricata Alerts Drops** | Line Chart    | Biểu đồ chuỗi thời gian đếm số lượng cảnh báo Alert và sự kiện Drop của Suricata. |
| **Top Sources**           | Bar Chart     | Top 15 địa chỉ IP nguồn bị Firewall chặn nhiều nhất.                              |
| **Top Destination Ports** | Bar Chart     | Top 15 Cổng dịch vụ (Destination Port) bị Firewall chặn nhiều nhất.               |
| **DoS Candidates**        | Table         | Phát hiện các IP nguồn nghi vấn tấn công DoS/Scan Port (bị chặn ≥ 50 lần).        |
| **SNMP Status**           | Table         | Bảng kiểm tra trạng thái thu thập dữ liệu SNMP chi tiết của từng thông số.        |
