# 02 EC2 생성과 보안 그룹

AWS Console 화면의 문구는 시점과 계정에 따라 조금 다를 수 있습니다. 버튼 이름이
다르면 같은 의미의 `Launch instance`, `Instances`, `Security groups` 메뉴를
찾습니다.

## 1. Region 확인

수업에서 정한 Region을 선택합니다. 생성 후 다른 Region으로 이동하면 인스턴스가
보이지 않는 것처럼 느낄 수 있으므로 화면 상단의 Region을 기록합니다.

```text
사용 Region: ____________________
```

## 2. 인스턴스 생성

1. AWS Console에서 EC2를 엽니다.
2. `Instances`를 선택합니다.
3. `Launch instances`를 선택합니다.
4. 이름을 `multi-agent-simple-compose`로 지정합니다.
5. 최신 Amazon Linux 2023 x86_64 AMI를 선택합니다.
6. Console에서 현재 계정에 적합한 최소 Instance Type을 선택합니다.
7. 새 Key Pair를 만들거나 강사가 지정한 Key Pair를 선택합니다.
8. Root EBS의 `Delete on termination` 설정을 확인합니다.
9. Public IPv4가 할당되는 네트워크 설정인지 확인합니다.

## 3. Key Pair

Key 파일은 다시 내려받기 어려우므로 안전한 로컬 폴더에 저장합니다.

금지:

- Git 저장소에 Commit
- 메신저·공용 Drive 공유
- README에 Key 내용 붙여넣기
- EC2 서버 내부에 Private Key 업로드

Windows 예시 경로:

```text
C:\Users\<사용자>\.ssh\multi-agent-course.pem
```

실제 사용자 이름으로 바꾸고 Key 파일 경로를 문서나 Git에 저장하지 않습니다.

## 4. Security Group

다음 두 Inbound Rule만 사용합니다.

| Type | Port | Source | 목적 |
| --- | ---: | --- | --- |
| SSH | 22 | My IP | 관리자 접속 |
| Custom TCP | 8503 | My IP | Streamlit 화면 |

다음 Rule은 만들지 않습니다.

```text
22    0.0.0.0/0
8200  0.0.0.0/0
```

IP가 변경되어 SSH 접속이 안 되면 SSH Rule의 Source를 현재 `My IP`로
갱신합니다. 문제 해결을 위해 22번 포트를 전체 인터넷에 열지 않습니다.

## 5. 생성 후 기록

```text
Instance ID: ____________________
Public IPv4: ____________________
Public DNS:  ____________________
Security Group ID: ______________
Root Volume ID: __________________
```

민감한 Secret은 아니지만 제출 문서에는 계정 식별 정보가 과도하게 노출되지
않도록 일부를 마스킹합니다.

## 6. 접속 전 확인

```text
[ ] Instance 상태가 running
[ ] Status check가 통과
[ ] Public IPv4가 있음
[ ] SSH Source가 My IP
[ ] 8503 Source가 My IP
[ ] 8200 Inbound Rule이 없음
```

## 공식 문서

- [EC2 Security Group 생성](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-security-group.html)
- [Security Group Rule 변경](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/changing-security-group.html)

