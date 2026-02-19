# Insight-Miner

간결하고 깔끔한 개발자 포트폴리오 스타일의 프로젝트 소개서입니다. 이 저장소는 멀티모달 문서(특히 PDF)에서 텍스트, 표, 이미지를 추출하고 분석하는 연구/프로토타입 코드와 문서를 포함합니다.
# Insight-Miner

간단한 개발자 포트폴리오 스타일 README입니다. 이 저장소는 멀티모달 문서(특히 PDF)를 파싱하여 텍스트, 표, 이미지에서 구조화된 데이터를 추출하고 분석하는 프로토타입 코드를 포함합니다.

한눈에 보기

- 역할: 멀티모달 문서 파싱 · 임베딩 · 검색 · 분석 데모
- 목적: 복잡한 보고서(표/차트 포함)에서 신뢰 가능한 구조화 데이터와 분석 결과를 얻기 위한 실험

주요 기능

- PDF 파싱 (텍스트 · 표 · 이미지)
- 표 및 이미지의 구조화/요약 추출
- ChromaDB 기반 벡터 저장 및 RAG 검색
- 질의에 따라 Python 코드를 실행하는 분석 워크플로우

기술 스택

- Python 3.10+
- LangChain / LlamaIndex (LlamaParse) 또는 unstructured
- ChromaDB
- Streamlit (간단한 데모 UI)
- pandas

파일/구조

- `agent.py`, `ingestion.py`, `rag_chain.py`, `storage.py`, `main.py` — 핵심 코드
- `requirements.txt` — 의존성
- `.env.example` — 환경변수 템플릿 (실제 키는 커밋하지 마세요)

빠른 시작

```bash
git clone https://github.com/junny311/insight-miner.git
cd insight-miner
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
```

환경 변수 설정

```text
# 복사: .env.example -> .env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
LLAMA_CLOUD_API_KEY=YOUR_LLAMA_API_KEY
```

데모 실행

```bash
streamlit run main.py
```

주의

- 민감한 키는 `.env`에 보관하더라도 절대 커밋하지 마세요.
- 대용량 바이너리(데이터베이스, 원본 PDF, 파싱 캐시 등)는 저장소에서 제거했습니다. 로컬이나 안전한 스토리지에 보관하세요.

원하시면 README에 데모 스크린샷/사용 예시를 추가하거나, 코드를 `src/`로 정리하고 간단한 테스트를 추가해 드리겠습니다.
```

