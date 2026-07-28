# 06 Security

Agent별 Tool allowlist를 결정적 Python 코드로 검사합니다.

```powershell
python .\tool_policy.py
```

Supervisor는 Agent 선택과 상태 조회만 허용되며 결제·예약·삭제 Tool은 사용할 수
없습니다. LLM이 Tool 사용을 요청해도 allowlist 검사를 통과해야 실행됩니다.
