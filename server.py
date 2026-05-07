#!/usr/bin/env python3
"""간단한 MCP 서버 - 수업 실습용"""

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
import httpx


app = Server("simple-mcp-server")


@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="read_github_file",
            description="GitHub 리포지토리에서 파일 내용을 읽어옵니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub 저장소 URL (예: https://github.com/owner/repo)"},
                    "branch": {"type": "string", "description": "브랜치 이름 (기본값: main)"},
                    "file_path": {"type": "string", "description": "파일 경로 (예: src/main.py)"}
                },
                "required": ["repo_url", "file_path"]
            }
        ),
        Tool(
            name="subtract",
            description="두 숫자의 뺄셈 결과를 계산합니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "첫 번째 숫자"},
                    "b": {"type": "number", "description": "두 번째 숫자"}
                },
                "required": ["a", "b"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "read_github_file":
        return await read_github_file(
            arguments["repo_url"],
            arguments.get("branch", "main"),
            arguments["file_path"]
        )
    elif name == "subtract":
        return subtract(arguments["a"], arguments["b"])
    else:
        raise ValueError(f"Unknown tool: {name}")


async def read_github_file(repo_url: str, branch: str, file_path: str) -> list[TextContent]:
    """GitHub에서 파일 내용을 읽어옵니다"""
    try:
        # URL에서 owner/repo 추출
        parts = repo_url.rstrip("/").split("/")
        if "github.com" in parts:
            idx = parts.index("github.com")
            owner = parts[idx + 1]
            repo = parts[idx + 2].replace(".git", "")
        else:
            raise ValueError("유효하지 않은 GitHub URL입니다")

        # Raw 파일 URL 생성
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"

        async with httpx.AsyncClient() as client:
            response = await client.get(raw_url)
            response.raise_for_status()

        return [TextContent(type="text", text=response.text)]

    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"파일을 찾을 수 없습니다: {e}")]
    except Exception as e:
        return [TextContent(type="text", text=f"오류 발생: {str(e)}")]


def subtract(a: float, b: float) -> list[TextContent]:
    """두 숫자의 뺄셈 결과를 반환합니다"""
    result = a - b
    return [TextContent(type="text", text=f"결과: {a} - {b} = {result}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
