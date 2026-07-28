# 09 Failure, Retry and Fallback

## 학습 목표

- retry·fallback·replan·escalation을 구분합니다.
- 오류 유형별 횟수 제한을 적용합니다.
- fallback 사용 사실을 결과와 Trace에 표시합니다.

## 실행

```powershell
python .\09_failure-retry-and-fallback\01_retry_example.py
python .\09_failure-retry-and-fallback\02_fallback_example.py
```

정책 위반은 retry하지 않고 즉시 차단합니다. 같은 오류를 무제한 반복하지
않습니다.

## 완료 체크

- 일시적 오류와 영구 오류를 구분합니다.
- 실패 후 사람이 판단해야 하는 조건을 설명합니다.

