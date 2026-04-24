import os
import streamlit as st
import json
from datetime import datetime
from openai import OpenAI

print("----------> 重新执行此文件，渲染展示页面")

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="AI 陪伴助手",
    page_icon="🤗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== 路径配置 ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")
RESOURCE_DIR = os.path.join(BASE_DIR, "resource")

# ==================== 工具函数 ====================
def save_session():
    """保存当前会话信息到 JSON 文件"""
    if st.session_state.current_session:
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": st.session_state.messages
        }
        if not os.path.exists(SESSIONS_DIR):
            os.makedirs(SESSIONS_DIR)
        session_file = os.path.join(SESSIONS_DIR, f"{st.session_state.current_session}.json")
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)


def generate_session_id():
    """生成基于当前时间的会话唯一标识"""
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")


def load_sessions():
    """加载所有会话文件列表"""
    session_list = []
    if os.path.exists(SESSIONS_DIR):
        for filename in os.listdir(SESSIONS_DIR):
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    return session_list


def load_session(session_name):
    """加载指定会话记录到 session_state"""
    try:
        session_file = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        if os.path.exists(session_file):
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
                st.session_state.messages = session_data["messages"]
                return True
        return False
    except Exception as e:
        st.error(f"加载会话失败: {str(e)}")
        return False


def delete_session(session_name):
    """删除指定的会话文件及对应状态"""
    try:
        session_file = os.path.join(SESSIONS_DIR, f"{session_name}.json")
        if os.path.exists(session_file):
            os.remove(session_file)
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_id()
            return True
        return False
    except Exception as e:
        st.error(f"删除会话失败: {str(e)}")
        return False


def get_session_stats():
    """获取当前会话的统计信息"""
    total = len(st.session_state.messages)
    user_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
    ai_count = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    return total, user_count, ai_count


# ==================== 性格预设模板 ====================
personality_templates = {
    "🌸 温柔女生": {
        "nick_name": "小甜甜",
        "nature": "南方温柔女生性格，说话轻声细语，善解人意，会关心你的情绪"
    },
    "💼 知心姐姐": {
        "nick_name": "知心姐",
        "nature": "成熟稳重，善于倾听和给出建议，像大姐姐一样可靠"
    },
    "🎉 活泼小伙伴": {
        "nick_name": "小太阳",
        "nature": "开朗幽默，喜欢开玩笑，充满活力和正能量"
    },
    "🌙 治愈系男友": {
        "nick_name": "阿暖",
        "nature": "温暖体贴，会关心你的情绪，给你安全感和依靠"
    },
    "📚 文艺青年": {
        "nick_name": "墨言",
        "nature": "喜欢诗词文学，说话有文化气息，浪漫且有深度"
    },
    "🐱 萌宠系": {
        "nick_name": "喵喵",
        "nature": "可爱俏皮，喜欢用颜文字和emoji，让人心情愉悦"
    }
}

# ==================== 系统初始化 ====================
st.title("AI 陪伴助手")
st.logo("logo.png")

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

system_prompt = """
你叫%s，是用户的专属陪伴伙伴，全程以温柔治愈的身份和用户聊天。

规则：
1. 每次只回复1条消息，不一次性说多句。
2. 禁止任何场景、动作或状态描述性文字，只输出对话内容。
3. 完全匹配用户的语言风格，用户说啥你就顺着聊啥。
4. 回复简短自然，像微信聊天一样轻松日常。
5. 可以适量使用 ❤️🌸✨ 这类软萌emoji，别太多。
6. 保持温柔暖心的性格，语气温柔不敷衍，会认真倾听用户的情绪。
7. 全程以陪伴式的语气对话，不暴露自己是AI，不使用“我是AI”这类表述。
8. 回复要温暖治愈，给用户安心感，像一个贴心的朋友。
    助手性格：%s

必须严格遵循以上规则来回复用户
"""

# ==================== Session State 初始化 ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小甜甜"

if "nature" not in st.session_state:
    st.session_state.nature = "南方温柔女生性格"

if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_id()

# ==================== 侧边栏 ====================
with st.sidebar:
    st.subheader("AI控制面板")

    # 新建会话
    if st.button("新建会话", width="stretch", icon="✏️"):
        if st.session_state.messages:
            save_session()
        st.session_state.messages = []
        st.session_state.current_session = generate_session_id()
        save_session()
        st.rerun()

    # 会话历史
    st.text("会话历史")
    session_list = load_sessions()
    session_list.sort(reverse=True)  # 按时间倒序

    for session in session_list:
        col1, col2 = st.columns([5, 1])
        with col1:
            btn_type = "primary" if session == st.session_state.current_session else "secondary"
            if st.button(session, width="stretch", icon="📄", key=f"load_{session}", type=btn_type):
                if st.session_state.messages:
                    save_session()
                load_session(session)
                st.rerun()
        with col2:
            if st.button("", width="stretch", icon="❌️", key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    st.divider()
    st.subheader("陪伴助手信息")

    # 性格预设模板
    selected_template = st.selectbox(
        "🎭 选择性格模板",
        list(personality_templates.keys()),
        index=None,
        placeholder="请选择性格"
    )
    if selected_template:
        if st.button("应用模板", width="stretch", type="primary"):
            st.session_state.nick_name = personality_templates[selected_template]["nick_name"]
            st.session_state.nature = personality_templates[selected_template]["nature"]
            st.success(f"✅ 已应用模板：{selected_template}")
            st.rerun()

    # 自定义昵称和性格
    nick_name = st.text_input("昵称:", placeholder="请输入昵称", value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name

    nature = st.text_area("性格:", placeholder="请输入性格", value=st.session_state.nature, height=100)
    if nature:
        st.session_state.nature = nature

# ==================== 主界面 ====================
st.text(f"💬 会话：{st.session_state.current_session}")

# 显示统计信息
total, user_count, ai_count = get_session_stats()
st.markdown(f"""
    <div style='font-size: 12px; color: #888; margin-bottom: 10px;'>
        📊 总消息数: {total} | 我的消息: {user_count} | AI回复: {ai_count}
    </div>
""", unsafe_allow_html=True)

# 展示聊天历史
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 聊天输入框
prompt = st.chat_input("来和我说说吧，我一直都在哦~")
if prompt:
    st.chat_message("user").write(prompt)
    print("----------> 调用AI大模型 提示词:", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner(f"{st.session_state.nick_name}正在思考..."):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
                    *st.session_state.messages,
                ],
                stream=True
            )

            # 流式输出
            with st.chat_message("assistant"):
                response_message = st.empty()
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        response_message.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            print("<---------- AI大模型返回结果:", full_response)
            save_session()
        except Exception as e:
            error_msg = f"抱歉，出现了一些问题：{str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            save_session()
