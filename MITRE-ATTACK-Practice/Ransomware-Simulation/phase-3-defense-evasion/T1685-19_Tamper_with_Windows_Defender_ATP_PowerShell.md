T1685-19 Tamper with Windows Defender ATP PowerShell
**1. Executive Summary**
Trong phiên kiểm thử SOC/SOAR Home Lab, thực hiện mô phỏng kỹ thuật MITRE ATT&CK T1685 - Disable or Modify Tools bằng Atomic Red Team, bài test T1685-19 - Tamper with Windows Defender ATP PowerShell. T1685 mô tả hành vi vô hiệu hóa hoặc sửa đổi các công cụ bảo mật nhằm làm suy giảm khả năng phát hiện và bảo vệ của hệ thống.
Bài test sử dụng PowerShell và Set-MpPreference để thử thay đổi bốn chức năng bảo vệ của Microsoft Defender:
Set-MpPreference -DisableRealtimeMonitoring 1
Set-MpPreference -DisableBehaviorMonitoring 1
Set-MpPreference -DisableScriptScanning 1
Set-MpPreference -DisableBlockAtFirstSeen 1
Sysmon, LimaCharlie EDR và Splunk đã ghi nhận đầy đủ process, user context và command line. Custom rule LC - Windows Defender Tampering phát hiện đúng hành vi và alert được chuyển sang DFIR-IRIS để điều tra.
Kết luận: True Positive - Authorized Simulation. Hành vi Defender tampering được thực thi và phát hiện thành công trong môi trường lab có kiểm soát.
**2. Incident Classification**
| Hạng mục | Kết quả |
| --- | --- |
| Case Name | T1685-19 - Tamper with Windows Defender ATP PowerShell |
| Classification | True Positive - Authorized Simulation |
| Control Outcome | Microsoft Defender settings modified successfully |
| MITRE Tactic | Defense Evasion |
| MITRE Technique | T1685 - Disable or Modify Tools |
| Atomic Test | Test #19 - Tamper with Windows Defender ATP PowerShell |
| Detection Sources | Sysmon, Splunk, LimaCharlie EDR |
| Case Platform | DFIR-IRIS |
| Affected Host | DESKTOP-JI0TPU0 |
| User | DESKTOP-JI0TPU0\longday |
| Observed Time Window | 22/07/2026, 14:21:16–14:21:24 |
| Business Impact | None |
| Containment Required | No |
| Final Status | Ready for closure after cleanup |

**3. ****Scope**** ****and**** ****Environment**
Bài kiểm thử được thực hiện trên Windows 10 victim trong môi trường home lab có kiểm soát, phục vụ mục tiêu:
Kiểm tra khả năng phát hiện hành vi can thiệp Microsoft Defender.
Xác thực telemetry giữa Sysmon và LimaCharlie EDR.
Kiểm tra pipeline Splunk → DFIR-IRIS.
Thực hành quy trình triage và investigation cho kỹ thuật Defense Evasion.

![img_007_cee25e7b](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_007_cee25e7b.png)

Kiểm tra alert trên DFIR-IRIS thì phát hiện 6 alert lần lượt được đẩy lên trong cùng 1 khung thời gian và tiến hành kiểm tra phần raw log được đẩy lên trong từng alert và tôi phát hiện Tag HIGH được gắn trên các alert và **risk_score:**70 nên tôi tiến hành tự assign và merge thành case và bắt đầu phân tích luôn.

![img_005_28365db7](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_005_28365db7.png)

![img_003_2a0a062c](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_003_2a0a062c.png)

Mở Dashboard EDR Limacharlie trên splunk xem xét xem thời gian có trùng khớp với lúc báo alert avf phát hiện trong mục **Suspicious**** ****Process**** ****Executions**** **đang có xuất hiện 1 tiến trình chạy bằng powershell. Và tiến hành đánh dấu tạm mốc thời gian và kiểm tra kỹ hơn qua các index.

![img_001_0ecf0ebe](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_001_0ecf0ebe.png)

**4. Detection Overview**
Sau khi Atomic Red Team thực thi bài test, LimaCharlie EDR ghi nhận các event liên quan đến:
- HOSTNAME.EXE
- whoami.exe
- powershell.exe
- conhost.exe
SecurityHealthHost.exeCác detection xuất hiện trong cùng time window gồm:
- Suspicious Execution of Hostname
- Local Accounts Discovery
- LC - Windows Defender Tampering
Trong đó, rule **LC - Windows Defender Tampering** là detection chính, match command line chứa bốn tham số sửa đổi Microsoft Defender.

5. Technical Timeline
Đối chiếu dữ liệu trên LimaCharlie EDR với index=win10sysmon, xác định chuỗi hoạt động chính của bài test T1685-19 – Tamper with Windows Defender ATP PowerShell diễn ra trong khoảng thời gian từ 14:21:16 đến 14:21:24 ngày 22/07/2026.
![img_009_d41d1db5](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_009_d41d1db5.png)

**Map**** ATT&CK T1685 ****-**** ****Disable**** ****or**** ****Modify**** ****Tools**
1.Atomic Red Team khởi chạy các tiến trình HOSTNAME.EXE và whoami.exe nhằm xác định hostname, user context và môi trường đang thực thi bài test.
2.Một tiến trình powershell.exe mới được tạo với PID 9656, có parent là một tiến trình PowerShell khác. Đây là tiến trình thực thi payload chính của bài test.
3.PowerShell lần lượt gọi bốn lệnh Set-MpPreference:
- Set-MpPreference -DisableRealtimeMonitoring 1
- Set-MpPreference -DisableBehaviorMonitoring 1
- Set-MpPreference -DisableScriptScanning 1
- Set-MpPreference -DisableBlockAtFirstSeen 1
4.Các lệnh trên nhằm làm suy yếu nhiều lớp bảo vệ của Microsoft Defender, bao gồm:
- Real-time monitoring.
- Behavior monitoring.
- PowerShell/script scanning.
- Block at First Seen.
5.Trong quá trình PowerShell thực thi, file tạm dạng __PSScriptPolicyTest_*.ps1 được tạo trong thư mục %TEMP%. Đây là artifact thường xuất hiện khi PowerShell kiểm tra chính sách thực thi script.
6.Nhiều tiến trình consent.exe được ghi nhận ngay sau khi payload chạy. Sự kiện này phù hợp với việc bài Atomic yêu cầu quyền nâng cao và Windows kích hoạt thành phần xử lý UAC.

![img_008_b5a5a742](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_008_b5a5a742.png)

Timeline
| Giờ | PID | Sự kiện | Ý nghĩa |
| --- | --- | --- | --- |
| 14:21:16 | 8632 | HOSTNAME.EXE được khởi chạy | Xác định hostname của endpoint |
| 14:21:16 | 2220 | whoami.exe được khởi chạy | Xác định user context đang thực thi bài test |
| 14:21:18 | 8768 | powershell.exe được tạo | Payload chính của Atomic Red Team bắt đầu thực thi |
| 14:21:18 | 8768 | Thực thi DisableRealtimeMonitoring 1 | Vô hiệu hóa giám sát thời gian thực |
| 14:21:18 | 8768 | Thực thi DisableBehaviorMonitoring 1 | Vô hiệu hóa giám sát hành vi |
| 14:21:18 | 8768 | Thực thi DisableScriptScanning 1 | Vô hiệu hóa chức năng quét script |
| 14:21:18 | 8768 | Thực thi DisableBlockAtFirstSeen 1 | Vô hiệu hóa Block at First Seen |
| 14:21:18 | 4060 | conhost.exe được tạo | Console host phục vụ PowerShell session |
| 14:21:18 | 7772, 6628 | HOSTNAME.EXE được chạy thêm | Atomic Red Team tiếp tục xác nhận thông tin endpoint |
| 14:21:18 | 8632, 2220 | Các process kiểm tra ban đầu kết thúc | Hoàn tất bước thu thập user và hostname |
| 14:21:20 | 8768 | powershell.exe kết thúc | Payload hoàn thành việc sửa bốn thiết lập Defender |
| 14:21:20 | 4060, 6628, 7772 | Các process con kết thúc | Chuỗi thực thi ngắn hạn được dọn dẹp |
| 14:21:22 | 5984 | SecurityHealthHost.exe được tạo | Windows Security cập nhật hoặc phản ánh trạng thái bảo vệ sau thay đổi |
| 14:21:24 | 5984 | SecurityHealthHost.exe kết thúc | Hoạt động cập nhật trạng thái hoàn tất |

Đối chiếu dữ liệu với các Index sysmon và edr trên Splunk trong khoảng thời gian tương tự và phát hiện các hoạt động đều log đúng

![img_006_36909c75](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_006_36909c75.png)

Các alert được Limacharlie đẩy lên splunk cũng theo thứ tự tương tự với các rule
Suspicious Execution of Hostname
Local Accounts Discovery
Suspicious Execution of Hostname
Và đặc biệt là 1 rule của tôi tạo ra cũng đã match rule đó là **LC - Windows ****Defender**** ****Tampering**** **đã phát hiện được hành vi dùng powershel để thực thì tắt giám sát hành vi, tắt quét các lệnh thực thi , và tắt tính năng bảo mật cực kỳ quan trọng nằm trong thành phần **Antivirus** của hệ điều hành Windows. Đây là cơ chế **giết nhầm còn hơn bỏ sót** dựa trên sức mạnh của điện toán đám mây để ngăn chặn các loại mã độc dạng *Zero**-**day.*

![img_004_6dcb43ab](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_004_6dcb43ab.png)

![img_002_315be51f](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_002_315be51f.png)

![img_010_148fc788](T1685-19_Tamper_with_Windows_Defender_ATP_PowerShell_images/img_010_148fc788.png)

**6. Process Chain Analysis**
Process chain quan sát được:
Invoke-AtomicTest
└── powershell.exe
├── HOSTNAME.EXE
├── whoami.exe
└── powershell.exe – PID 8768
├── Set-MpPreference -DisableRealtimeMonitoring 1
├── Set-MpPreference -DisableBehaviorMonitoring 1
├── Set-MpPreference -DisableScriptScanning 1
├── Set-MpPreference -DisableBlockAtFirstSeen 1
├── conhost.exe
└── HOSTNAME.EXE
**7. Defender State Validation**
**Trạng**** ****thái**** ****trước**** test**
DisableRealtimeMonitoring : False
DisableBehaviorMonitoring : False
DisableScriptScanning     : False
DisableBlockAtFirstSeen   : False
Điều này xác nhận bốn chức năng bảo vệ chưa bị vô hiệu hóa trước khi chạy Atomic test.
**Trạng**** ****thái**** ****sau**** test**
DisableRealtimeMonitoring : True
DisableBehaviorMonitoring : True
DisableScriptScanning     : True
DisableBlockAtFirstSeen   : True
**8. Network and IOC Review**
Bài test không tạo domain, IP, URL hoặc file hash độc hại cần enrichment qua MISP hoặc VirusTotal.
**9. ****Impact**** ****Assessment**
| Impact Area | Assessment |
| --- | --- |
| Security Control Tampering | Hành vi cố gắng can thiệp được xác nhận |
| Defender Configuration Change | 4 hành vi thay đổi được thực hiện |
| Endpoint Compromise | Không ghi nhận |
| Persistence | Không ghi nhận |
| Credential Access | Không ghi nhận |
| Lateral Movement | Không ghi nhận |
| C2 Communication | Không ghi nhận |
| Data Exfiltration | Không ghi nhận |
| Business Impact | None |

**10. Containment Decision**
**Quyết**** ****định**
- Containment Required: No
- Endpoint Isolation: Not required
- Process Kill: Not required
- Account Disable: Not required
- Defender Remediation: Verify configuration state
**Lý do**
- Hành vi được tạo bởi Atomic Red Team trong phạm vi kiểm thử.
- Hành vi được thực hiện bằng Atomic Red Team trong phạm vi kiểm thử.
- Không có external IOC.
- Không ghi nhận payload độc hại, persistence hoặc lateral movement.
