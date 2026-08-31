# Windows Docker 사전 준비

이 문서는 `01_simple-compose`를 시작하기 전에 한 번만 진행합니다. 강의실·회사 PC는
Windows 기능 변경이 제한될 수 있으므로 수업 전에 관리자 권한을 확인합니다.

## 1. 현재 상태 확인

일반 PowerShell에서 실행합니다.

```powershell
docker version
docker compose version
wsl --status
```

| 결과 | 다음 행동 |
| --- | --- |
| Docker Client와 Server가 모두 표시됨 | 01 Simple Compose로 이동 |
| `docker` 명령을 찾지 못함 | WSL 2 확인 후 Docker Desktop 설치 |
| WSL 선택 기능이 필요하다는 메시지 | 아래 Windows 기능 활성화 |
| 회사 정책·관리자 권한 오류 | 임의 우회하지 말고 관리자 또는 강사에게 요청 |

## 2. WSL 2 기능 활성화

PowerShell을 **관리자 권한으로 실행**한 뒤 다음 두 기능을 활성화합니다.

```powershell
dism.exe /online /Enable-Feature /FeatureName:Microsoft-Windows-Subsystem-Linux /All /NoRestart
dism.exe /online /Enable-Feature /FeatureName:VirtualMachinePlatform /All /NoRestart
```

두 명령이 끝나면 Windows를 재시작합니다. 이미 활성화된 기능에 같은 명령을 다시
실행해도 됩니다.

재시작 후 일반 PowerShell:

```powershell
wsl --update
wsl --set-default-version 2
wsl --status
```

## 3. Docker Desktop 설치

[Docker Desktop Windows 공식 설치 안내](https://docs.docker.com/desktop/setup/install/windows-install/)에서
지원 Windows 버전, WSL 요구 사항, 조직의 사용 조건을 확인하고 설치합니다.
설치 화면에서는 Linux Container용 WSL 2 백엔드를 사용합니다.

Docker Desktop을 실행한 뒤 새 PowerShell에서 확인합니다.

```powershell
docker version
docker compose version
docker run --rm hello-world
```

`docker version`에서 Client만 나오고 Server 연결 오류가 보이면 Docker Desktop이
아직 시작 중이거나 실행되지 않은 것입니다.

## 4. 수업 전 체크

```text
[ ] 관리자 권한 또는 담당자 지원이 준비되었다.
[ ] WSL 기본 버전이 2이다.
[ ] Docker Desktop이 실행 중이다.
[ ] docker version에서 Client와 Server를 확인했다.
[ ] docker compose version을 확인했다.
[ ] hello-world Container가 종료 코드 0으로 끝났다.
```

Docker Desktop 설치가 불가능한 PC에서는 01의 코드를 읽고 GitHub Actions의 Linux
Runner 결과를 관찰할 수 있지만, 로컬 Container 실습 완료로 표시하지 않습니다.
