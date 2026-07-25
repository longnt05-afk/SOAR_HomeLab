# Windows Endpoint Security & Threat Hunting Dashboard

## Mục đích (Purpose)

Dashboard này phục vụ công tác giám sát an ninh chi tiết trên các máy trạm và máy chủ Windows bằng cách tổng hợp dữ liệu từ **Windows Security Event Log**, **Sysmon** và **PowerShell Operational Log**. Dashboard cho phép phân tích viên SOC theo dõi các sự kiện an ninh quan trọng (Event Code 4625, 4624, 1102...), phát hiện hành vi lạm dụng các công cụ hệ thống (LOLBins - Living off the Land Binaries), nhận diện các đoạn mã PowerShell độc hại bị mã hóa hoặc tải ngoài, đồng thời giám sát các truy vấn DNS và kết nối mạng nghi vấn trên endpoint.

---

## Nguồn dữ liệu (Data Source)

- **Index:** `win10eventlog`, `win10sysmon`, `win10powershell` (Gom nhóm qua Macro `win_indexes`)
- **Sourcetype:** `XmlWinEventLog:Security`, `XmlWinEventLog:Microsoft-Windows-Sysmon/Operational`, `XmlWinEventLog:Microsoft-Windows-PowerShell/Operational`
- **Format:** Windows Event Log XML / Structured Log

---

## Bố trí và Chức năng các Panel (Panel Layout)

| Tên Panel                       | Kiểu hiển thị | Chức năng & Nghiệp vụ                                                                     |
| :------------------------------ | :------------ | :---------------------------------------------------------------------------------------- |
| **Security Events**             | Single Value  | Tổng số lượng sự kiện ghi nhận từ Windows Security Log.                                   |
| **Sysmon Events**               | Single Value  | Tổng số lượng sự kiện ghi nhận từ nhật ký Sysmon.                                         |
| **PowerShell 4104**             | Single Value  | Tổng số lượng bản ghi Script Block Logging (Event Code 4104) từ PowerShell.               |
| **LOLBin Count**                | Single Value  | Số lượng tiến trình thực thi lạm dụng công cụ hệ thống (certutil, bitsadmin, mshta...).   |
| **Suspicious PowerShell Count** | Single Value  | Số lượng mã lệnh PowerShell nghi vấn (chứa encodedcommand, iex, downloadstring...).       |
| **Windows Timeline**            | Line Chart    | Biểu đồ chuỗi thời gian biến động lượng log mỗi 30 phút phân theo từng Index.             |
| **Windows Signal Mix**          | Pie Chart     | Tỷ lệ phân bổ dữ liệu giữa Security Event Log, Sysmon và PowerShell Log.                  |
| **Security EventCodes**         | Bar Chart     | Top 12 mã Event Code xuất hiện nhiều nhất trong Windows Security Log.                     |
| **Sysmon EventCodes**           | Bar Chart     | Top 12 mã Event Code xuất hiện nhiều nhất trong nhật ký Sysmon.                           |
| **Top Windows Hosts**           | Bar Chart     | Top 10 máy trạm / máy chủ Windows phát sinh nhiều log nhất.                               |
| **High Value Windows Events**   | Table         | Bảng 50 sự kiện an ninh nguy cơ cao (1102, 4625, 4672, 4720...) phân cấp độ Risk.         |
| **LOLBin Executions**           | Table         | Danh sách 50 hành vi khởi chạy LOLBin nghi vấn kèm Command Line, Parent Image và Hash.    |
| **Suspicious PowerShell**       | Table         | Bảng 50 đoạn mã PowerShell chứa các hàm nguy hiểm nghi vấn mã hóa hoặc độc hại.           |
| **DNS Queries**                 | Table         | Top 40 tên miền được truy vấn nhiều nhất từ Sysmon Event Code 22 kèm tiến trình khởi tạo. |
| **Process Network Connections** | Table         | Top 40 kết nối mạng xuất phát từ tiến trình trên Windows (Sysmon Event Code 3).           |
