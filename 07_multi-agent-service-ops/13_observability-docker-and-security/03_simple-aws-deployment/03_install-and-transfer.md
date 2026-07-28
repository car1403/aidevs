# 03 Docker 설치와 코드 전송

## 1. SSH 접속

로컬 PowerShell에서 실제 Key 경로와 Public DNS로 바꿉니다.

```powershell
ssh -i "C:\Users\<사용자>\.ssh\multi-agent-course.pem" ec2-user@<PUBLIC_DNS>
```

첫 연결에서는 서버 지문을 확인하는 질문이 나타날 수 있습니다. 대상 Public DNS가
본인이 만든 인스턴스와 일치하는지 먼저 확인합니다.

## 2. Docker Engine 설치

EC2 터미널에서 실행합니다.

```bash
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
```

그룹 변경을 적용하려면 SSH 연결을 종료하고 다시 접속합니다.

```bash
exit
```

재접속 후 확인합니다.

```bash
docker info
```

권한 오류가 계속되면 Docker 서비스 상태를 확인하고, 필요하면 교육 담당자의
안내에 따라 인스턴스를 재부팅합니다.

## 3. Docker Compose Plugin

먼저 설치 여부를 확인합니다.

```bash
docker compose version
```

명령이 없다면 RPM 기반 Linux의 Docker Compose Plugin 설치를 시도합니다.

```bash
sudo yum update -y
sudo yum install -y docker-compose-plugin
docker compose version
```

패키지를 찾지 못하면 임의 블로그 명령을 실행하지 말고
[Docker 공식 Linux Compose 설치 문서](https://docs.docker.com/compose/install/linux/)를
확인합니다. 수동 설치는 자동 업데이트되지 않으므로 강사가 버전을 지정한 경우에만
사용합니다.

## 4. 코드 전송 방법 A: 공개 교육 저장소

저장소가 공개되어 있고 Secret이 없을 때만 사용합니다.

```bash
git clone <PUBLIC_REPOSITORY_URL> aidevs
cd aidevs/07_multi-agent-service-ops/13_observability-docker-and-security/01_simple-compose
```

Private Repository 인증 Token을 명령이나 Git URL에 직접 넣지 않습니다.

## 5. 코드 전송 방법 B: SCP

저장소 공개가 불가능하면 Simple Compose 폴더만 전송합니다.

로컬 PowerShell:

```powershell
scp -i "C:\Users\<사용자>\.ssh\multi-agent-course.pem" -r `
  "C:\aidevs\07_multi-agent-service-ops\13_observability-docker-and-security\01_simple-compose" `
  ec2-user@<PUBLIC_DNS>:~/simple-compose
```

EC2 터미널:

```bash
cd ~/simple-compose
ls
```

다음 파일이 보여야 합니다.

```text
backend
frontend
docker-compose.yml
README.md
```

## 공식 문서

- [Amazon Linux 2023 EC2에 Docker 설치](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-container-image.html)
- [Docker Compose Plugin 설치](https://docs.docker.com/compose/install/linux/)

