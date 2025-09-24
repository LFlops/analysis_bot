import asyncio
import agentscope
from agentscope.agent import ReActAgent
from agentscope.mcp import StdIOStatefulClient
from agentscope.model import OpenAIChatModel
from agentscope.tool import Toolkit
from agentscope.formatter import OpenAIChatFormatter

# 初始化 AgentScope
agentscope.init(
    project="okx-agent"
)

# 配置模型
model = OpenAIChatModel(
    model_name="gpt-3.5-turbo",
    api_key="YOUR_OPENAI_API_KEY"  # 替换为你的 API Key
)


async def main():
    # 连接到 MCP 服务器
    mcp_client = StdIOStatefulClient(
        name="okx-mcp-client",
        command="python",
        args=["okx_mcp_server.py"]
    )
    
    # 连接客户端
    await mcp_client.connect()

    # 创建工具包
    toolkit = Toolkit()
    await toolkit.register_mcp_client(mcp_client)

    # 创建一个 Agent，并为其配备工具
    # ReActAgent 是一个很好的选择，因为它能够进行"思考-行动-观察"循环
    # 从而决定何时以及如何调用工具
    analyst_agent = ReActAgent(
        name="CryptoAnalyst",
        sys_prompt="你是一个专业的加密货币市场分析师，能够使用工具获取实时的币价和历史K线数据。请根据用户需求进行分析和报告。如果你需要价格数据，请调用 get_crypto_price 工具。如果你需要历史数据来分析趋势，请调用 get_kline_data 工具。",
        model=model,
        formatter=OpenAIChatFormatter(),
        toolkit=toolkit,
    )

    # 启动对话
    while True:
        prompt = input("请输入你的分析需求（例如：分析一下 BTC/USDT 最近一小时的价格走势，输入 'exit' 退出）：")
        if prompt.lower() == 'exit':
            break

        # Agent 开始执行任务
        try:
            response = await analyst_agent(prompt)
            print("Agent 的分析结果：\n", response.content)
        except Exception as e:
            print(f"分析过程中出现错误: {e}")
    
    # 关闭客户端连接
    await mcp_client.close()


if __name__ == "__main__":
    asyncio.run(main())
