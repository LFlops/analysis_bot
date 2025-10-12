#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OKX MCP Server implementation
"""
import asyncio
import json
import os
import sys
from typing import Any

import ccxt
from dotenv import load_dotenv
from mcp.server import InitializationOptions
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ListToolsResult

load_dotenv()
# 从环境变量或配置文件加载你的 OKX API 凭证
api_key = os.getenv('OKX_API_KEY')
secret_key = os.getenv('OKX_API_SECRET')
passphrase = os.getenv('OKX_API_PASSPHRASE')
print(api_key, secret_key, passphrase)

# --- 启动前检查环境变量 ---
if not all([api_key, secret_key, passphrase]):
    print(
        "错误: 缺少必要的OKX环境变量。请确保 "
        "OKX_API_KEY, OKX_API_SECRET, 和 OKX_API_PASSPHRASE "
        "都已在 .env 文件中正确设置。",
        file=sys.stderr
    )
    sys.exit(1)

# 初始化 OKX 交易所客户端
okx = ccxt.okx({
    'apiKey': api_key,
    'secret': secret_key,
    'password': passphrase,  # ccxt中password对应passphrase
    'options': {
        'defaultType': 'spot',  # 默认为现货交易
    }
})


def get_crypto_price(symbol: str) -> dict:
    """
    获取指定交易对的最新价格。

    Args:
        symbol (str): 交易对，如 'BTC/USDT'。

    Returns:
        dict: 包含最新价格、24小时最高价和最低价等信息。
    """
    try:
        ticker = okx.fetch_ticker(symbol)
        price_info = {
            "symbol": ticker['symbol'],
            "last_price": ticker['last'],
            "high_24h": ticker['high'],
            "low_24h": ticker['low'],
            "change_24h_percent": ticker['percentage']
        }
        return price_info
    except Exception as e:
        return {"error": str(e)}


def get_kline_data(symbol: str, timeframe: str = '1h', limit: int = 100) -> list:
    """
    获取指定交易对的 K 线数据。

    Args:
        symbol (str): 交易对，如 'BTC/USDT'。
        timeframe (str): 时间周期，如 '1h' (1小时), '1d' (1天)。
        limit (int): 返回的 K 线数量。

    Returns:
        list: K 线数据列表。
    """
    try:
        k_lines = okx.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        # 格式化数据，方便后续分析
        formatted_data = [
            {"timestamp": k[0], "open": k[1], "high": k[2], "low": k[3], "close": k[4], "volume": k[5]}
            for k in k_lines
        ]
        return formatted_data
    except Exception as e:
        return [{"error": str(e)}]


async def serve(srv: Server) -> None:
    # 注册工具
    @srv.list_tools()
    async def list_tools() -> ListToolsResult:
        return ListToolsResult(
            tools=[
                Tool(
                    name="get_crypto_price",
                    description="获取指定交易对的最新价格",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "交易对，如 'BTC/USDT'"
                            }
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="get_kline_data",
                    description="获取指定交易对的 K 线数据",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "交易对，如 'BTC/USDT'"
                            },
                            "timeframe": {
                                "type": "string",
                                "description": "时间周期，如 '1h' (1小时), '1d' (1天)",
                                "default": "1h"
                            },
                            "limit": {
                                "type": "number",
                                "description": "返回的 K 线数量",
                                "default": 100
                            }
                        },
                        "required": ["symbol"]
                    }
                )
            ]
        )

    @srv.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        try:
            if name == "get_crypto_price":
                result = get_crypto_price(arguments["symbol"])
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]
            elif name == "get_kline_data":
                result = get_kline_data(
                    arguments["symbol"],
                    arguments.get("timeframe", "1h"),
                    arguments.get("limit", 100)
                )
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]
            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            # 确保即使在错误情况下也返回正确的类型
            error_result = {"error": str(e)}
            return [TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False))]


async def main():
    # 创建 MCP 服务器实例
    async with stdio_server() as (read_stream, write_stream):
        srv = Server(name="okx-mcp-server")
        await serve(srv)
        await srv.run(
                read_stream, write_stream,
                InitializationOptions(
                    server_name="okx-mcp-server",
                    server_version="0.1.0",
                    capabilities={},
                ))


if __name__ == "__main__":
    asyncio.run(main())
