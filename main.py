import agentscope
from agentscope.agents import ReActAgent
from agentscope.mcp import McpClient

# 初始化 AgentScope
agentscope.init(
    model_configs=[
        # 这里配置你的大模型，例如 OpenAI、DashScope 等
        {
            "model_type": "openai",
            "config_name": "gpt-3.5-turbo",
            "model_name": "gpt-3.5-turbo",
            "api_key": "YOUR_OPENAI_API_KEY" # 替换为你的 API Key
        }
    ]
)

# 连接到 MCP 服务器
mcp_client = McpClient(host="127.0.0.1", port=5000)

# 创建一个 Agent，并为其配备工具
# ReActAgent 是一个很好的选择，因为它能够进行"思考-行动-观察"循环
# 从而决定何时以及如何调用工具
analyst_agent = ReActAgent(
    name="CryptoAnalyst",
    model_config_name="gpt-3.5-turbo",
    tools=[mcp_client.get_tool_group()],
    sys_prompt="你是一个专业的加密货币市场分析师，能够使用工具获取实时的币价和历史K线数据。请根据用户需求进行分析和报告。如果你需要价格数据，请调用 get_crypto_price 工具。如果你需要历史数据来分析趋势，请调用 get_kline_data 工具。"
)

def run_analysis(prompt):
    """执行单次分析任务"""
    response = analyst_agent(prompt)
    return response.content

if __name__ == "__main__":
    # 启动对话
    while True:
        prompt = input("请输入你的分析需求（例如：分析一下 BTC/USDT 最近一小时的价格走势，输入 'exit' 退出）：")
        if prompt.lower() == 'exit':
            break

        # Agent 开始执行任务
        try:
            result = run_analysis(prompt)
            print("Agent 的分析结果：\n", result)
        except Exception as e:
            print(f"分析过程中出现错误: {e}")
