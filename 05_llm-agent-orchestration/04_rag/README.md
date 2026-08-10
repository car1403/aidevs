# 04 RAG

## 학습 목표

- LLM의 내부 지식과 외부 문서 검색을 구분합니다.
- 문서 분할, 검색, Context 생성, 답변의 흐름을 설명합니다.
- 검색 근거가 없을 때 답변을 제한합니다.
- 사용자에게 출처를 표시합니다.

## 기본과 확장

```text
기본: API Key 없는 단어 기반 검색
확장: Embedding + Vector Store
실제 연동: Docker PostgreSQL + pgvector + Ollama embedding
```

먼저 검색과 근거 제시라는 RAG의 핵심을 확인한 뒤 저장 기술을 교체합니다.

## 실행

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
python .\03_pgvector_ollama_example.py
```

`03`은 `00_local-runtime`의 컨테이너와 DB Schema를 먼저 준비해야 합니다.
Embedding 생성은 Ollama, Vector 저장·유사도 검색은 pgvector가 담당합니다.
