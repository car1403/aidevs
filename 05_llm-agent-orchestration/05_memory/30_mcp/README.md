# 30 · HTTP MCP Memory

기존 Python Memory 로직을 Agent가 호출할 수 있는 MCP Tool로 노출합니다. 전송 방식은
Streamable HTTP이며 기본 주소는 `http://127.0.0.1:8002/mcp`입니다.

## Tool

| Tool | 역할 | 변경 여부 |
| --- | --- | --- |
| `list_memories` | 현재 사용자 Memory 조회 | 읽기 |
| `save_memory` | 허용된 선호 저장·수정 | 쓰기 |
| `delete_memory` | Memory ID로 삭제 | 쓰기 |
| `find_relevant_memories` | 질문 관련 Memory 선택 | 읽기 |

Tool 인자에는 `user_id`가 없습니다. 이 서버는 `MCP_DEMO_USER_ID`를 인증 계층에서
확인된 사용자라고 가정하고, 해당 범위만 관리합니다.

## 실행

과정 루트에서 패키지를 설치한 후 Server를 실행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:MCP_DEMO_USER_ID="student-01"
python .\05_memory\30_mcp\memory_mcp_server.py
```

새 Terminal에서 최소 Client를 실행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration
.\.venv\Scripts\Activate.ps1
python .\05_memory\30_mcp\memory_mcp_client.py
```

순수 저장소 테스트는 MCP Server 없이 실행할 수 있습니다.

```powershell
python .\05_memory\30_mcp\test_memory_store.py
```

## Codex 연결

프로젝트의 `.codex/config.toml` 또는 사용자 `~/.codex/config.toml`에 다음을 추가하고
Codex를 다시 시작합니다.

```toml
[mcp_servers.memory_demo]
url = "http://127.0.0.1:8002/mcp"
enabled_tools = ["list_memories", "save_memory", "delete_memory", "find_relevant_memories"]
default_tools_approval_mode = "writes"
```

Codex 앱 설정에서도 MCP servers → Add server → Streamable HTTP를 선택하고 같은 URL을
입력할 수 있습니다.

## 인증 경계

이 예제는 localhost 수업용이므로 실제 로그인은 구현하지 않습니다. 운영 환경에서는
사용자가 Tool 인자로 보낸 ID를 신뢰하지 말고, OAuth 또는 Bearer Token을 검증한 뒤
서버가 확인한 사용자 ID로 저장소 범위를 정해야 합니다. Codex에서 Bearer Token을
전달할 때는 다음처럼 환경 변수 이름을 설정할 수 있습니다.

```toml
[mcp_servers.memory_production]
url = "https://memory.example.com/mcp"
bearer_token_env_var = "MEMORY_MCP_TOKEN"
default_tools_approval_mode = "writes"
```
