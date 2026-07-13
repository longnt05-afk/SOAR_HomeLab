# LimaCharlie Ransomware VIP Pro D&R Rules

This pack contains 7 D&R rules:

1. L1 User-writable suspicious execution - report/tag only.
2. L2 Office/browser/archive spawned suspicious shell - block child tree.
3. L3 Backup/shadow destruction - block launcher + isolate host.
4. L1 Suspicious filename created - report/tag only.
5. L2 Suspicious filename executed - block current tree.
6. L1 LOLBin download payload - report/tag only.
7. L2 LOLBin download payload with suspicious parent - block current tree.

Notes:

- No YARA is used in this pack.
- No automatic file deletion is used, so evidence is preserved.
- Use LimaCharlie timeline to confirm field paths if any rule does not trigger in your sensor version.
