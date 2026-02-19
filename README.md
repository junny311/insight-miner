# Insight-Miner

간결하고 깔끔한 개발자 포트폴리오 스타일의 프로젝트 소개서입니다. 이 저장소는 멀티모달 문서(특히 PDF)에서 텍스트, 표, 이미지를 추출하고 분석하는 연구/프로토타입 코드와 문서를 포함합니다.

## 한줄 요약

멀티모달 문서 분석 파이프라인 — PDF → 파싱 → 벡터 저장 → RAG/코드 기반 분석.

## 핵심 기능

- 멀티모달 파싱: 텍스트, 표, 이미지에서 구조화된 데이터 추출
- 멀티 벡터 검색: ChromaDB 기반 벡터 저장 및 검색
- 동적 분석 엔진: 질의에 따라 RAG 또는 Python 실행기로 전환
- Streamlit UI: 간단한 데모용 웹 인터페이스

## 기술 스택

- Python 3.10+
- LangChain, LlamaIndex (LlamaParse) / unstructured
- ChromaDB
- Streamlit
- pandas
- python-dotenv

## 리포지토리 구조

- `agent.py`, `ingestion.py`, `rag_chain.py`, `storage.py`, `main.py` — 핵심 소스 코드
- `requirements.txt` — 의존성
- `.env.example` — 환경변수 템플릿 (실제 키는 커밋하지 마세요)

## 빠른 시작

1. 리포지토리 클론

```bash
git clone https://github.com/junny311/insight-miner.git
cd insight-miner
```

2. 가상환경 생성 및 활성화

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

4. 환경 변수 설정

```text
# 복사: .env.example -> .env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
LLAMA_CLOUD_API_KEY=YOUR_LLAMA_API_KEY
```

5. 데모 실행 (Streamlit)

```bash
streamlit run main.py
```

## 주의 및 정리

- 대용량 바이너리(데이터베이스, PDF, 파싱 결과 등)는 저장소에서 제거했습니다. 관련 데이터는 로컬에서 관리하세요.
- `.env` 파일에 민감한 키를 저장하지 말고, 깃에 업로드하지 마세요. 필요 시 GitHub Secrets 또는 CI 환경 변수를 사용하세요.

## 다음 단계(권장)

- 코드 정리: 모듈을 `src/`로 분리, 테스트 추가
- 데모 영상/스크린샷 추가 (README 상단)
- 간단한 예제 노트북 또는 스크린샷으로 사용법 문서화

---

문의: 저장소 정리를 더 진행하거나 README 스타일/문구를 세부 조정할까요?
