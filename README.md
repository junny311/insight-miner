# Insight-Miner (멀티모달 문서 분석 AI Agent)

## 🚀 프로젝트 개요

Insight-Miner는 복잡한 PDF 문서(재무제표, 기술 보고서 등)에서 텍스트 정보는 물론, **복잡한 표(Table)**와 **차트(Image)**를 구조화된 데이터로 추출하여 분석하는 AI Agent 프로젝트입니다. 단순한 정보 검색(RAG)을 넘어, 내장된 Python Code Interpreter를 활용하여 실제 수치 연산 및 데이터 분석을 수행할 수 있습니다.

## ✨ 주요 기능

*   **멀티모달 문서 분석**: PDF 내의 텍스트, 표, 이미지를 통합적으로 분석합니다.
*   **구조화된 데이터 추출**: LlamaParse를 활용하여 표를 Markdown 또는 HTML 형식으로, 이미지를 텍스트 요약(Image Description)으로 추출합니다.
*   **멀티 벡터 검색**: ChromaDB를 사용하여 텍스트 청크, 표 요약본, 이미지 설명을 벡터화하여 저장하고 검색합니다. 원본 데이터는 별도로 저장하여 LLM에 주입 시 정보 손실을 방지합니다.
*   **지능형 Agent & 추론 엔진**: 사용자 질문을 분석하여 일반적인 질의에는 RAG(Retrieval-Augmented Generation)를, 수치 계산이나 데이터 분석이 필요한 질문에는 Python Code Interpreter를 동적으로 활용합니다.
*   **Python Code Interpreter**: LLM이 직접 수치 계산을 암산하지 않고, Python 코드를 생성하고 실행하여 정확한 분석 결과를 도출합니다.
*   **사용자 친화적 UI**: Streamlit을 통해 PDF 업로드, 파싱, 벡터 저장, 그리고 Agent와의 질의응답을 지원하는 인터페이스를 제공합니다.

## 🛠️ 기술 스택 (Strict)

*   **Language**: Python 3.10+
*   **Framework**: LangChain (최신 버전)
*   **Parsing**: LlamaParse (또는 Unstructured)
*   **Vector DB**: ChromaDB (Multi-vector Storage)
*   **LLM**: GPT-4o (Reasoning & Code Generation)
*   **UI**: Streamlit
*   **Data Analysis**: Pandas
*   **Environment**: python-dotenv

## ⚙️ 시스템 아키텍처 및 데이터 파이프라인

1.  **Ingestion (데이터 주입 & 파싱)**
    *   복합 PDF 문서를 입력받아 LlamaParse를 통해 Raw Text, Tables (Markdown/HTML), Images (PNG -> Text Summary)로 분리합니다.

2.  **Storage (저장 전략 - Multi-Vector Retriever)**
    *   **Vector Store**: 텍스트 청크, 테이블의 요약본(Summary), 이미지의 설명(Caption)을 임베딩하여 검색에 활용합니다.
    *   **Document Store**: 원본 테이블(Markdown)과 원본 이미지 경로를 저장하여 LLM Context 주입 시 사용합니다.
    *   **메커니즘**: 요약본으로 검색하되, LLM에는 원본(구조화된 표)을 전달하여 정보 손실을 방지합니다.

3.  **Agent & Reasoning (추론 엔진)**
    *   사용자 질문을 분석하여 Router가 적절한 도구를 선택합니다.
    *   **일반 질문**: RAG 검색 결과를 바탕으로 답변을 생성합니다.
    *   **분석/연산 질문**: Python Code Interpreter (Pandas DataFrame Agent 또는 Python REPL Tool)를 호출하여 수치 연산 및 데이터 분석을 수행합니다. LLM은 수치 계산을 직접 하지 않고 반드시 코드를 생성 및 실행합니다.

## 🚀 시작하기

### 📋 사전 준비

1.  **리포지토리 클론**:
    ```bash
    git clone https://github.com/youngjun498/insight-miner.git
    cd insight-miner
    ```

2.  **가상 환경 설정**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **의존성 설치**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **.env 파일 설정**:
    프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 필요한 API 키를 설정합니다. (예: LlamaParse API Key, Google API Key 등)

    ```
    LLAMAPARSE_API_KEY="YOUR_LLAMAPARSE_API_KEY"
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    # 기타 필요한 환경 변수들
    ```

### ▶️ 프로젝트 실행

모든 설정이 완료되면, 다음 명령어를 통해 Streamlit 애플리케이션을 실행할 수 있습니다.

```bash
streamlit run main.py
```

브라우저에서 애플리케이션이 열리면, PDF 문서를 업로드하고 Agent와 상호작용할 수 있습니다.
