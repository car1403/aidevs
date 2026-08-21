# 04 RAG 실습

## 독립 Lab 구성

모든 Lab은 실제 pgvector를 사용합니다. Redis가 필요한 Lab은 실제 TTL Cache와
Namespace 무효화를 사용하며, Agent에게 DB·SQL·Redis 명령을 직접 제공하지 않습니다.

| Lab | 시나리오 | 핵심 학습 |
|---:|---|---|
| 01 | 고객지원 정책 Agent | Tool Call, pgvector 검색, Redis Cache |
| 02 | 정책 문서 갱신 | 재색인, 오래된 Chunk 제거, Cache 무효화 |
| 03 | 쇼핑몰 상품 검색 | Metadata Filter, 가격·카테고리 조건, Hybrid Search |
| 04 | 사내 규정 문서 | 사용자 권한별 문서 검색, ACL Filter |
| 05 | PDF 여행 가이드 | PDF Chunking, 페이지 출처, 중복 색인 방지 |
| 06 | 검색 품질 평가 | Hit@K, MRR, Keyword·Vector·Hybrid 비교 |
| 07 | Multi-Tool RAG Agent | 재질문, 여러 지식 저장소 선택, 종료 조건 |

## 독립 Lab 1. 고객지원 RAG Agent

`01_customer_support_rag_agent.py`는 `03_tool-use`의 Agent와 Tool 실행 원칙을 실제
pgvector·Redis RAG에 연결합니다.

```text
질문 → Agent의 검색 Tool Call 제안 → Backend Allowlist·Pydantic 검증
→ pgvector 검색 → Tool Result → Ollama 근거 답변 → Redis TTL Cache
```

```powershell
cd C:\aidevs\05_llm-agent-orchestration\04_rag
python .\10_labs\01_customer_support_rag_agent.py

# 실제 Ollama Tool Calling으로 Agent의 선택을 확인할 때
$env:RAG_LAB_AGENT_PROVIDER="ollama"
python .\10_labs\01_customer_support_rag_agent.py
```

첫 실행은 pgvector 검색과 답변 생성을 수행하는 Cache MISS이고, 같은 질문의 두 번째
실행은 Redis Cache HIT입니다. Redis를 중지하면 Cache 저장은 실패하지만 pgvector
검색과 답변 생성은 계속됩니다.

확인할 항목:

1. Agent의 Tool Call과 Backend가 실행한 Tool Result를 구분합니다.
2. 허용되지 않은 Tool과 잘못된 `query`, `top_k`가 실행 전에 차단되는지 확인합니다.
3. 답변의 출처가 `파일명#Chunk 번호`로 표시되는지 확인합니다.
4. 첫 호출의 `cache_hit=False`와 두 번째 호출의 `cache_hit=True`를 확인합니다.
5. Redis 장애가 장기 문서 저장소인 pgvector 검색을 막지 않는지 확인합니다.

## 독립 Lab 2. 정책 문서 갱신과 Cache 무효화

`02_document_update_and_cache_invalidation.py`는 정책 문서의 새 버전을 pgvector에
Upsert하고, 새 문서에서 사라진 이전 Chunk를 제거한 뒤 관련 Redis Cache만
무효화하는 결정적 Workflow입니다.

```text
version 1 색인·Cache 무효화 → 검색 MISS·HIT → version 2 Upsert
→ 오래된 Chunk 제거·전용 Redis Namespace 무효화 → 새 검색 MISS
```

```powershell
cd C:\aidevs\05_llm-agent-orchestration\04_rag
python .\10_labs\02_document_update_and_cache_invalidation.py
```

문서 갱신 순서와 Cache 무효화는 정해진 업무 규칙이므로 Agent가 판단하지 않습니다.
Backend Workflow가 처리하며, 사용자 질문에 답할 때만 Agent가 검색 Tool을 선택합니다.

확인할 항목:

1. version 1의 두 Chunk가 pgvector에 저장되는지 확인합니다.
2. 동일 질문의 Redis Cache MISS→HIT를 확인합니다.
3. 한 Chunk로 줄어든 version 2를 색인한 뒤 이전 두 번째 Chunk가 제거되는지 확인합니다.
4. 각 문서 변경 후 `FLUSHDB`가 아니라 이 Lab의 Cache Namespace만 SCAN·삭제하는지 확인합니다.
5. version 2 색인 직후 같은 질문이 새 정책을 검색하고 다시 MISS가 되는지 확인합니다.

## 독립 Lab 3. 쇼핑몰 상품 Hybrid Search

```powershell
python .\10_labs\03_product_hybrid_search.py
```

실제 상품을 pgvector에 저장하고 카테고리는 JSONB Metadata Filter로, 최대 가격은
검증된 Backend 조건으로 제한합니다. 키워드와 벡터 순위는 RRF로 결합하고 검색 조건
전체를 Redis Cache Key에 포함합니다.

확인할 항목:

1. `category=shoes`, `max_price=100000` 밖의 상품이 제외되는지 확인합니다.
2. 상품 코드에 강한 키워드 검색과 설명에 강한 벡터 검색을 비교합니다.
3. 단위가 다른 점수를 더하지 않고 RRF 순위를 사용하는지 확인합니다.

## 독립 Lab 4. 사내 규정 ACL 검색

```powershell
python .\10_labs\04_internal_policy_acl_search.py
```

사용자 역할은 Agent arguments가 아니라 인증된 Backend 세션에서 가져옵니다. pgvector
검색 SQL에 JSONB ACL Filter를 적용하고, Redis Cache Key에도 역할을 포함합니다.

확인할 항목:

1. 일반 직원이 HR 전용 문서를 검색할 수 없는지 확인합니다.
2. Agent가 Tool arguments로 자신의 역할을 변경할 수 없는지 확인합니다.
3. 서로 다른 역할이 동일한 Cache Entry를 공유하지 않는지 확인합니다.

## 독립 Lab 5. PDF 여행 가이드

```powershell
python .\10_labs\05_pdf_travel_guide.py C:\data\travel-guide.pdf --query "박물관 휴관일은?"
```

텍스트형 PDF를 페이지별 Chunk로 나누어 pgvector에 저장합니다. 파일명·페이지 번호·파일
Hash를 Metadata로 보존하며, 같은 PDF를 다시 색인해도 결정적 Chunk ID로 갱신합니다.

확인할 항목:

1. 검색 결과에 원본 파일명과 페이지 번호가 표시되는지 확인합니다.
2. 동일 파일 재색인 시 Chunk가 중복 증가하지 않는지 확인합니다.
3. 문서가 짧아졌을 때 오래된 Chunk가 제거되는지 확인합니다.
4. 스캔 PDF에 OCR이 필요한 이유를 설명합니다.

## 독립 Lab 6. 검색 품질 평가

```powershell
python .\10_labs\06_retrieval_quality_evaluation.py
```

질문과 정답 문서 ID로 구성된 작은 평가 Dataset을 사용합니다. 실제 Keyword·pgvector·
Hybrid 검색 결과에서 Hit@3와 MRR을 계산하여 유사도 점수 자체가 아니라 정답 순위를
비교합니다.

확인할 항목:

1. 정답이 Top-K에 포함되는 비율과 정답의 평균 역순위를 구분합니다.
2. 검색 방식별 실패 질문과 정답 순위를 비교합니다.
3. `top_k`를 변경하고 Hit@K와 MRR의 변화를 관찰합니다.

## 독립 Lab 7. Multi-Tool RAG Agent

```powershell
python .\10_labs\07_multi_tool_rag_agent.py
```

첫 Cycle의 모호한 요청에는 답을 추측하지 않고 호텔·항공·관광 중 필요한 영역을
재질문합니다. 다음 사용자 입력에서 상태를 병합한 뒤 서로 분리된 pgvector Collection의
검색 Tool을 호출하고 근거 답변을 Redis에 캐싱합니다.

확인할 항목:

1. 모호한 첫 요청이 `clarification_required`로 종료되는지 확인합니다.
2. 두 번째 Cycle에서 호텔과 항공 Tool만 호출되는지 확인합니다.
3. Tool별 Allowlist와 Pydantic arguments 검증을 확인합니다.
4. `MAX_STEPS`, 전체 Trace, `termination_reason`을 확인합니다.
5. Agent가 Collection 이름이나 SQL을 직접 선택하지 않는지 확인합니다.

## 실행 위치

실습 1~3은 Backend와 Docker 없이 실행합니다. 실습 4의
`06_pgvector_ollama_example.py`는 Mini Backend를 호출하지 않고 PostgreSQL·pgvector와
Ollama에 직접 연결합니다.

```powershell
cd C:\mini_agent_st\infra
docker compose up -d postgres redis ollama
docker compose exec ollama ollama pull embeddinggemma
```

완성 RAG 화면을 확인할 때만 별도 터미널에서 다음 Backend를 실행합니다.

```powershell
cd C:\mini_agent_st\mini_agent_04_rag\backend
uvicorn app.main:app --reload --port 8000
```

## 실습 1. Chunk 크기 비교

`02_chunking_and_metadata.py`의 `sentences_per_chunk`를 1, 2, 4로 바꾸고 Chunk 개수와 내용을 비교합니다.

## 실습 2. 검색 결과 설명하기

`03_keyword_retrieval.py`에서 `top_k`를 1과 3으로 실행하고, 검색 결과가 늘어날 때 Context에 불필요한 내용이 섞일 수 있는 이유를 적습니다.

## 실습 3. 근거 없음 처리

등록되지 않은 여권 분실 질문을 입력하고 다음을 확인합니다.

- `grounded`가 `False`인가?
- `sources`가 비어 있는가?
- 문서에 없는 내용을 추측하지 않는가?

## 실습 4. 실제 pgvector 검색

Docker 환경을 실행한 후 `06_pgvector_ollama_example.py`의 질문을 세 가지로 바꿉니다.

- 호텔 예약을 취소하고 싶어요.
- 비행기에 가방을 몇 kg까지 실을 수 있나요?
- 박물관이 쉬는 날은 언제인가요?

각 질문에서 1위 문서와 점수를 기록합니다.

## 실습 5. 키워드와 pgvector 비교

`07_keyword_vs_pgvector.py`에서 두 검색 방식의 1위 문서와 점수를 기록하고 의미가
비슷하지만 단어가 다른 질문에서 결과가 달라지는 이유를 설명합니다.

## 실습 6. 실제 LLM 근거 답변

`08_real_rag_answer.py`를 준비된 Provider로 실행하고 답변이 출력된 Context와 출처로
뒷받침되는지 확인합니다.

## 실습 7. Redis Cache

`09_redis_rag_cache.py`로 MISS→HIT와 TTL을 확인합니다. `top_k`나 Provider를 바꾸면
새 Cache Key가 사용되는지 확인하고 재색인 후 다시 MISS가 되는지 관찰합니다.

## 실습 8. 직접 입력 문장 검색

`11_text_insert_and_search.py`에 의미는 비슷하지만 단어가 다른 문장과 질문을 각각
추가합니다. `top_k`와 `score_threshold`를 바꾸며 관련 없는 결과가 제거되는지 확인합니다.

## 실습 9. PDF 페이지 출처 검색

텍스트형 PDF를 준비하고 `12_pdf_index_and_search.py`로 색인합니다. 서로 다른 페이지의
내용을 묻는 질문 세 개를 실행하여 1위 Chunk의 파일명, 페이지 번호, 점수를 기록합니다.
같은 PDF를 다시 색인했을 때 Chunk 수가 중복 증가하지 않는지도 확인합니다.

> 이미지로 스캔된 PDF는 이 기본 실습의 대상이 아닙니다. 텍스트가 추출되지 않을 때
> OCR이 필요한 이유를 설명하는 것은 심화 실습으로 다룹니다.

## 실습 10. Agent와 pgvector Tool

`13_agent_pgvector_tool.py`를 먼저 기본 `mock` 모드로 실행하여 Tool Call과 Tool Result를
확인합니다. 이후 `RAG_AGENT_PROVIDER=ollama`로 실행하여 실제 Agent가 검색 Tool을
선택하는지, 최종 답변이 Tool Result와 출처로 뒷받침되는지 비교합니다.

## 실습 11. Metadata Filter와 임계값

`14_metadata_and_threshold.py`에서 `category`, `status`, `language` 조건을 하나씩 제거해
만료되었거나 다른 범주의 문서가 검색되는지 관찰합니다. `score_threshold`를 여러 값으로
바꾸고 관련 문서까지 사라지는 지점을 기록하여 임계값의 정밀도·재현율 trade-off를
설명합니다.

## 실습 12. Hybrid Search와 RRF

`15_hybrid_search.py`의 질문에서 정확한 객실 코드가 있는 경우와 없는 경우를 비교합니다.
키워드, pgvector, Hybrid 각각의 상위 문서를 기록하고 `rank_constant`를 바꿨을 때 RRF
순위가 어떻게 변하는지 확인합니다.
