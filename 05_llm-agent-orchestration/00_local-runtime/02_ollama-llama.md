# Docker Ollama와 Llama

## 실행

CPU 기준:

```powershell
docker run -d `
  --name aidevs-ollama `
  -p 11434:11434 `
  -v aidevs-ollama-data:/root/.ollama `
  ollama/ollama
```

## 모델 준비

```powershell
docker exec -it aidevs-ollama ollama pull llama3.2
docker exec -it aidevs-ollama ollama list
```

모델명은 PC 사양과 수업 시점에 따라 변경할 수 있도록 `.env`의 `OLLAMA_MODEL`에서 관리합니다.

## API 확인

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:11434/api/chat `
  -ContentType "application/json" `
  -Body '{"model":"llama3.2","messages":[{"role":"user","content":"부산 여행을 한 문장으로 소개해 주세요."}],"stream":false}'
```

## 학습 포인트

- GPT·Gemini는 Cloud API이고 Ollama/Llama는 Local 실행입니다.
- 모델 파일은 Docker Volume에 저장합니다.
- Structured Output과 Tool Calling 지원은 선택한 모델에 따라 확인해야 합니다.
- 로컬 실행이라고 해서 입력 검증과 권한 검사가 불필요한 것은 아닙니다.
