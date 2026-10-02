# AuditLog

누가 언제 무엇을 어떻게 바꿨는지(변경 전 → 후, 사유, 승인자)를 시간순으로 보여주는 변경 이력이다.

- **entries**: `{at, zone, actor, role, action, field, before, after, reason, approver}`.
- 금액 변경, 마감 재개방, 승인·반려는 반드시 사유와 승인자를 같이 남긴다.
- 현장 입력은 `zone: "ULAT"`, 본사 처리는 `"KST"`로 기록한다.
