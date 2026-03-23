# Insight-Miner 🔍

**멀티모달 문서 분석 AI Agent** — 복잡한 PDF(텍스트 · 표 · 차트)를 추출·임베딩·검색·분석하는 엔드-투-엔드 RAG 시스템.

<br>

## 📋 Project Overview

최신 금융 보고서, 기술 문서, 법제 자료 등 **구조화된 데이터를 포함한 복잡한 PDF**에서 신뢰 가능한 정보를 추출하는 것은 여전히 도전과제입니다. 단순 텍스트 검색(RAG)만으로는 표의 수치나 차트의 의미를 정확히 이해하기 어렵습니다.

**Insight-Miner**는 이 문제를 해결하기 위해 설계되었습니다:
- 🔄 **멀티모달 파싱**: 텍스트, 표, 이미지를 독립적으로 추출 및 처리
- 🎯 **하이브리드 검색**: 의미 기반 임베딩 + 원본 데이터 구조 보존
- 🐍 **동적 분석**: Python Code Interpreter를 통한 실시간 데이터 분석
- 🚀 **엔터프라이즈급 UI**: Streamlit 기반 반응형 웹 인터페이스

<br>

## 🏗️ System Architecture

```
┌─────────────────┐
│  Upload PDF     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Ingestion Layer (LlamaParse)      │
├─────────────────────────────────────┤
│ • Text  Chunks                      │
│ • Tables (Markdown)                 │
│ • Images (PNG desc)                 │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│    Storage Layer (ChromaDB)         │
├─────────────────────────────────────┤
│ Vector Store:                       │
│ ├─ Text embeddings                  │
│ ├─ Table summaries                  │
│ └─ Image captions                   │
│                                     │
│ Doc Store:                          │
│ ├─ Raw tables (Markdown)            │
│ └─ Image paths (cache)              │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Agent & Reasoning (LangChain)       │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │  Question Router (Gemini)       │ │
│ └────────┬────────────────────────┘ │
│          │                          │
│    ┌─────┴──────┐                  │
│    ▼            ▼                  │
│  [RAG]      [Python REPL]          │
│  Query      Code Gen & Run         │
│  Retrieval  Numerical Analysis     │
└────────┬───────────────────────────┘
         │
         ▼
    Final Answer
```

**핵심 설계 결정:**
- **Multi-Vector Retrieval**: 검색은 "요약본"으로 하되, LLM에 제공하는 정보는 "원본 구조화 표"를 사용 → 정보 손실 최소화
- **Hybrid Tool Routing**: 일반 질의는 RAG, 분석 질의는 Python 코드 생성 실행 → 정확도 향상
- **LLM 기반 라우팅**: 수치 계산을 LLM 암산에 의존하지 않고 코드 실행 결과 활용

<br>

## ✨ Key Features

| Feature | Description | Use Case |
|---------|-------------|----------|
| **멀티모달 추출** | PDF에서 텍스트, 표, 이미지 자동 분리 | 재무제표, 기술 보고서 분석 |
| **의미 기반 검색** | 자연어 질의로 관련 정보 자동 검색 | "2024년 매출은?" → 관련 섹션 자동 추출 |
| **동적 코드 생성** | 복잡한 분석용 Python 코드 자동 생성 및 실행 | "2023년 대비 2024년 성장률" 계산 |
| **대화형 분석** | 문서에 대한 자유로운 질의응답 | 보고서 내용에 대한 심화 질문 |
| **구조화 저장소** | 원본 데이터의 구조 보존 | 정확한 테이블/차트 참조 |

<br>

## 🛠️ Tech Stack & Design Rationale

| Component | Technology | Why? |
|-----------|-----------|------|
| **Parsing** | [LlamaParse](https://www.llamaindex.ai/llamaparse) | 표/이미지 추출에서 SOTA 성능, 마크다운 형식 지원 |
| **Vector DB** | ChromaDB | 경량 + 하이브리드 검색(텍스트+벡터) 지원, 로컬 배포 용이 |
| **LLM** | Google Gemini 2.5 Flash | 비용 효율적, 멀티모달 처리, 한국어 지원 우수 |
| **Framework** | LangChain | LCEL의 파이프라인 구성, 100+ 통합 라이브러리 |
| **UI** | Streamlit | 빠른 프로토타입, 상태 관리 용이, 배포 간편 |
| **Code Exec** | Python REPL | 신뢰 가능한 수치 계산, 디버깅 용이 |

<br>

## 🚀 Getting Started

### 1️⃣ Prerequisites

- Python 3.10+
- Google API Key (Generative AI)
- LlamaParse API Key (LlamaCloud)

### 2️⃣ Installation

```bash
# Clone the repository
git clone https://github.com/junny311/insight-miner.git
cd insight-miner

# Create virtual environment
python -m venv venv

# Activate (choose your OS)
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Environment Setup

```bash
# Create .env file from template
cp .env.example .env

# Edit .env with your API keys
GOOGLE_API_KEY=your_google_api_key
LLAMA_CLOUD_API_KEY=your_llama_api_key
```

### 4️⃣ Run the Application

```bash
streamlit run main.py
```

Access the app at **http://localhost:8501**

<br>

## 📁 Project Structure

```
insight-miner/
├── main.py                 # Streamlit UI & session management
├── ingestion.py            # LlamaParse로 PDF 파싱 (텍스트/표/이미지)
├── storage.py              # ChromaDB 저장 및 검색 관리
├── rag_chain.py            # RAG 체인 (retrieval + generation)
├── agent.py                # 라우팅 에이전트 & 도구 오케스트레이션
│
├── requirements.txt        # 의존성 목록
├── .env.example            # 환경변수 템플릿 (보안 주의!)
└── chroma_db/              # ChromaDB 로컬 저장소
```

**각 모듈의 역할:**

- **ingestion.py**: LlamaParse API를 호출하여 PDF를 마크다운 형식으로 변환
- **storage.py**: 임베딩된 청크를 ChromaDB에 저장 & 검색 인터페이스 제공
- **rag_chain.py**: LCEL 파이프라인으로 retriever + prompt + LLM 연결
- **agent.py**: 사용자 질문을 분석하여 RAG 또는 Python REPL로 라우팅
- **main.py**: Streamlit 애플리케이션 메인 루프 & 세션 상태 관리

<br>

## 💡 Usage Examples

### 예제 1: 문서 내용 검색
```
사용자: "매출의 주요 구성 요소는 무엇인가?"
→ RAG 도구 실행
→ 원본 표에서 매출 항목 검색 및 요약
```

### 예제 2: 수치 분석
```
사용자: "2023년과 2024년 매출 증가율을 계산해줄 수 있나?"
→ Python REPL 도구 실행
→ 자동 생성 코드: df['2024'] / df['2023'] - 1
→ 정확한 계산 결과 반환
```

### 예제 3: 데이터 시각화 (확장 가능)
```
사용자: "월별 매출 추이를 그려줘"
→ Python REPL
→ 자동 생성: matplotlib plot → 이미지 반환
```

<br>

## ⚙️ Configuration & Advanced Usage

### ChromaDB 설정

기본적으로 로컬 SQLite 저장소를 사용합니다. 프로덕션 환경에서는:

```python
# storage.py 수정 예시 (PostgreSQL 연동)
import chromadb

client = chromadb.HttpClient(host="chroma-server", port=8000)
```

### LLM 모델 전환

Gemini 대신 다른 LLM 사용:

```python
# rag_chain.py, agent.py
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)
```

### 임베딩 모델 커스터마이징

```python
# storage.py
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
```

<br>

## 🔒 Security & Best Practices

⚠️ **중요:**
- `.env` 파일은 절대 Git에 커밋하지 마세요 (`.gitignore`에 추가)
- API 키는 환경변수로만 관리하세요
- 프로덕션 배포 시 secrets manager 사용 (AWS Secrets, Azure Key Vault 등)

<br>

## 📊 Performance & Optimization

| Metric | Value | Note |
|--------|-------|------|
| 파싱 시간 | ~5-30초 | 문서 크기/복잡도에 따라 변동 |
| 검색 레이턴시 | <500ms | ChromaDB 로컬 검색 |
| 생성 시간 | 1-3초 | LLM API 응답 시간 포함 |
| 메모리 사용 | ~200-500MB | 임베딩 캐시 + 벡터 저장소 |

**최적화 팁:**
- 대용량 PDF는 챕터별로 분할 처리
- 배치 임베딩으로 처리 시간 단축
- 검색 결과 개수(k) 조정으로 품질/속도 트레이드오프 제어

<br>

## 🚧 Roadmap & Future Work

- [ ] 다국어 지원 강화 (한글 OCR 개선)
- [ ] 차트 인식 고도화 (차트 요약 요약 및 수치 추출)
- [ ] 대용량 문서 병렬 처리 (Ray 통합)
- [ ] 대시보드 고도화 (Plotly 차트, 내보내기 기능)
- [ ] API 서버화 (FastAPI + Docker)
- [ ] 정확도 평가 메트릭 (RAGAS 프레임워크)

<br>

## 📝 License

MIT License — 자유롭게 사용, 수정, 배포 가능합니다.

<br>

## 🤝 Contributing

이슈, 피드백, PR 환영합니다!

```bash
# 기여 방법
1. Fork this repository
2. Create feature branch (git checkout -b feature/amazing-feature)
3. Commit changes (git commit -m 'Add amazing feature')
4. Push to branch (git push origin feature/amazing-feature)
5. Open a Pull Request
```

<br>

## 📧 Contact & Support

- **Author**: [Your Name]
- **Email**: your.email@example.com
- **Issues**: [GitHub Issues](https://github.com/junny311/insight-miner/issues)

---

**Made with ❤️ by AI Engineering**
```

