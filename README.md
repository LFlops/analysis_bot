# OKX Agent

这是一个使用 AgentScope 构建的，能够灵活切换 **阿里通义千问** 和 **OpenAI GPT** 模型来分析加密货币价格的智能代理。

## 功能

- **动态模型支持**: 可通过环境变量在通义千问和 OpenAI 模型之间无缝切换。
- **实时价格查询**: 获取指定交易对的最新价格。
- **历史数据分析**: 获取 K 线数据用于趋势分析。
- **智能分析**: 基于强大的 ReAct Agent，能够根据用户需求自主调用工具并进行分析。

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

# 使用 uv 同步依赖 (会自动安装 dashscope)
uv pip sync pyproject.toml
```

### 2. 配置密钥

在运行程序之前，你需要配置 API 密钥。

**a. 复制环境变量文件**

```bash
cp .env.exemple .env
```

**b. 填入你的密钥**

编辑 `.env` 文件，填入你需要的 API 凭证。

```dotenv
# ----------------- OKX API Keys -----------------
OKX_API_KEY="your_api_key"
OKX_API_SECRET="your_api_secret"
OKX_API_PASSPHRASE="your_api_passphrase"

# ----------------- Model Provider Configuration -----------------
# 设置要使用的模型服务商，可选值为 "openai" 或 "dashscope"
MODEL_PROVIDER="dashscope"

# ----------------- LLM API Keys -----------------
# 填入你选择使用的模型对应的 API Key
DASHSCOPE_API_KEY="your_dashscope_api_key"
OPENAI_API_KEY="your_openai_api_key"
```

- 你可以在 [阿里云百炼平台](https://dashscope.console.aliyun.com/apiKey) 获取 `DASHSCOPE_API_KEY`。
- 你可以在 [OpenAI Platform](https://platform.openai.com/api-keys) 获取 `OPENAI_API_KEY`。

### 3. 运行程序

配置完成后，`uv run` 命令会自动加载 `.env` 文件中的配置来启动应用。

**a. 运行 (默认或指定DashScope)**

如果你的 `.env` 文件中 `MODEL_PROVIDER` 设置为 `"dashscope"`，或未设置（默认为dashscope），直接运行：

```bash
uv run --script okx-agent
```
> 程序将输出: `Using DashScope (Tongyi Qianwen) model.`

**b. 运行 (指定OpenAI)**

要临时切换到 OpenAI 模型，你可以在 `.env` 文件中修改 `MODEL_PROVIDER="openai"`，或者更方便地，在命令行中覆盖这个变量：

```bash
MODEL_PROVIDER=openai uv run --script okx-agent
```
> 程序将输出: `Using OpenAI model.`

程序启动后，你就可以在终端中输入你的分析指令了。