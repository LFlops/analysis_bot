# OKX Agent

这是一个使用 AgentScope 和 aio-mcp-server 构建的，用于分析加密货币价格的 OKX 代理。

## 功能

- **实时价格查询**: 获取指定交易对的最新价格。
- **历史数据分析**: 获取 K 线数据用于趋势分析。
- **智能分析**: 基于大语言模型（LLM）的 ReAct Agent，能够根据用户需求自主调用工具并进行分析。

## 如何运行

本项目推荐使用 `uv` 进行环境管理和依赖安装，因为它提供了极速的性能和便捷的工作流。

### 1. 环境准备

首先，请确保你已经安装了 Python 3.12+ 和 `uv`。

```bash
# 克隆项目仓库
git clone <your-repo-url>
cd okx-agent

# 使用 uv 创建并激活虚拟环境
uv venv
source .venv/bin/activate
# Windows 用户请使用: .\.venv\Scripts\activate

# 使用 uv 同步依赖
uv pip sync pyproject.toml
```

### 2. 配置密钥

在运行程序之前，你需要配置 OKX 和 OpenAI 的 API 密钥。

**a. 配置 OKX 密钥**

复制环境变量示例文件，并填入你自己的 OKX API 凭证。

```bash
cp .env.exemple .env
```

然后，编辑 `.env` 文件，替换其中的占位符。

```dotenv
OKX_API_KEY="your_api_key"
OKX_API_SECRET="your_api_secret"
OKX_API_PASSPHRASE="your_api_passphrase"
```

**b. 配置 OpenAI 密钥**

为了安全起见，强烈建议将你的 OpenAI 密钥也添加到 `.env` 文件中。

在 `.env` 文件末尾添加以下内容：

```dotenv
OPENAI_API_KEY="sk-..."
```

然后，修改 `main.py` 文件，使其从环境变量中读取该密钥。

```python
# main.py

# 在文件顶部添加
import os

# ...

# 找到模型配置部分并修改
model = OpenAIChatModel(
    model_name="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY") # 从环境变量读取
)
```

### 3. 运行程序

配置完成后，使用 `uv run` 命令启动应用。该命令会自动加载 `.env` 文件中的环境变量。

```bash
# 通过 pyproject.toml 中定义的脚本名运行
uv run --script okx-agent
```

或者，你也可以直接运行 `main.py` 文件：

```bash
uv run python main.py
```

程序启动后，你就可以在终端中输入你的分析指令了，例如：

> "分析一下 BTC/USDT 最近一小时的价格走势"

输入 `exit` 即可退出程序。
