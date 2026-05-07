import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="/home/kiyu/mcp-simple-server/venv/bin/python",
        args=["/home/kiyu/mcp-simple-server/server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("=== Tools List ===")
            tools = await session.list_tools()
            print(tools)

            print("\n=== Subtract Test ===")
            result = await session.call_tool("subtract", {"a": 10, "b": 3})
            print(result)

            print("\n=== GitHub File Read Test ===")
            result = await session.call_tool(
                "read_github_file",
                {
                    "repo_url": "https://github.com/python/cpython",
                    "branch": "main",
                    "file_path": "README.rst",
                },
            )
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
