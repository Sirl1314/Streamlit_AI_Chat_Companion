# AI 陪伴助手 🤗
一个基于 Streamlit + DeepSeek API 开发的个性化AI陪伴聊天助手，支持多性格预设、会话持久化、聊天统计等功能。

## 功能特性
✅ 多性格模板预设（温柔女生/知心姐姐/治愈系男友等6种风格）
✅ 会话持久化存储（自动保存/加载/删除聊天记录）
✅ 实时聊天统计（总消息数/用户消息数/AI回复数）
✅ 流式响应输出（模拟真实聊天的打字效果）
✅ 自定义AI昵称和性格描述
✅ 简洁美观的UI界面（侧边栏控制面板+主聊天区）

## 技术栈
- 前端/交互：Streamlit
- 后端：Python
- AI接口：DeepSeek API（OpenAI兼容）
- 数据存储：JSON文件（会话持久化）
- 环境管理：系统环境变量

## 快速开始
### 前置条件
- Python 3.8+
- DeepSeek API Key（从[DeepSeek官网](https://www.deepseek.com/)获取）

### 安装依赖
```bash
pip install streamlit openai python-dotenv