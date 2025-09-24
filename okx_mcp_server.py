import os
import ccxt
from agentscope.mcp import McpServer

# 从环境变量或配置文件加载你的 OKX API 凭证
api_key = os.getenv('OKX_API_KEY')
secret_key = os.getenv('OKX_API_SECRET')
passphrase = os.getenv('OKX_API_PASSPHRASE')

# 初始化 OKX 交易所客户端
okx = ccxt.okx({
    'apiKey': api_key,
    'secret': secret_key,
    'password': passphrase, # ccxt中password对应passphrase
    'options': {
        'defaultType': 'spot', # 默认为现货交易
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
        return {"error": str(e)}

if __name__ == "__main__":
    # 创建 MCP 服务器实例
    server = McpServer(
        host="127.0.0.1",
        port=5000,
        tool_functions=[get_crypto_price, get_kline_data]
    )
    # 启动 MCP 服务器
    server.run()
