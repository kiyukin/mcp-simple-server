# 간단한 MCP 서버 (수업 실습용)

MCP(Model Context Protocol) 서버의 기본 예제입니다.

## 설치 방법

```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
python server.py
```

## 제공되는 도구

### 1. read_github_file
GitHub 리포지토리에서 파일 내용을 읽어옵니다.

**입력:**
- `repo_url`: GitHub 저장소 URL
- `branch`: 브랜치 이름 (기본값: main)
- `file_path`: 파일 경로

**예시:**
```
repo_url: https://github.com/owner/repo
branch: main
file_path: src/main.py
```

### 2. subtract
두 숫자의 뺄셈을 계산합니다.

**입력:**
- `a`: 첫 번째 숫자
- `b`: 두 번째 숫자

**예시:**
```
a: 10
b: 3
```

## 테스트 예시

### subtract 테스트
```json
{
  "name": "subtract",
  "arguments": {
    "a": 10,
    "b": 3
  }
}
```

**응답:** `결과: 10 - 3 = 7`

### read_github_file 테스트
```json
{
  "name": "read_github_file",
  "arguments": {
    "repo_url": "https://github.com/python/cpython",
    "branch": "main",
    "file_path": "README.md"
  }
}
```

## 구조

```
mcp-simple-server/
├── server.py        # MCP 서버 코드
├── requirements.txt # 의존성
└── README.md        # 이 문서
```