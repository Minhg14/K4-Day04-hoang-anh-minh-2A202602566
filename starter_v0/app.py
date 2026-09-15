from __future__ import annotations

import streamlit as st
from pathlib import Path

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from chat import run_model_tool_loop, trim_history

# 1. Khởi tạo môi trường
ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)

st.set_page_config(page_title="IT Helpdesk Agent", page_icon="🤖", layout="wide")

# 2. Cấu hình trên Sidebar
with st.sidebar:
    st.header("⚙️ Cấu hình Agent")
    provider_name = st.selectbox(
        "Provider",
        options=["openrouter", "gemini", "openai", "anthropic"],
        index=0,
    )
    model_name = st.text_input("Model tùy chọn (để trống dùng mặc định):", value="")
    history_window = st.slider("Context History Window (cặp hội thoại)", min_value=1, max_value=10, value=5)
    max_tool_rounds = st.slider("Max Tool Rounds", min_value=1, max_value=10, value=4)

    if st.button("Xóa lịch sử chat"):
        st.session_state.chat_history = []
        st.session_state.display_messages = []
        st.rerun()

# 3. Cache tài nguyên cấu hình agent
@st.cache_resource
def init_agent_resources(p_name: str):
    system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    openai_tools = to_openai_tools(tool_declarations)
    provider_instance = make_provider(p_name)
    return system_prompt, openai_tools, provider_instance

try:
    system_prompt, openai_tools, provider = init_agent_resources(provider_name)
except Exception as e:
    st.error(f"Lỗi khởi tạo Provider '{provider_name}': {e}")
    st.stop()

# 4. Quản lý trạng thái Session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Lưu list các dict {"role": ..., "content": ...}

if "display_messages" not in st.session_state:
    st.session_state.display_messages = []  # Lưu để hiển thị lên UI kèm logs

st.title("🤖 IT Helpdesk Agent Web")

# Hiển thị lịch sử hội thoại
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tools" in msg and msg["tools"]:
            with st.expander("🛠️ Chi tiết các tool đã gọi"):
                st.json(msg["tools"])

# 5. Xử lý Input từ người dùng
if user_prompt := st.chat_input("Nhập câu hỏi hoặc báo sự cố thiết bị..."):
    # Hiển thị tin nhắn người dùng
    st.session_state.display_messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Chuẩn bị payload messages gửi vào loop
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.chat_history, history_window),
        {"role": "user", "content": user_prompt},
    ]

    with st.chat_message("assistant"):
        with st.spinner("Agent đang suy luận và gọi công cụ..."):
            try:
                selected_model = model_name.strip() or None
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=openai_tools,
                    model=selected_model,
                    max_tool_rounds=max_tool_rounds,
                )

                assistant_text = result.get("assistant_text", "")
                tool_events = result.get("tool_events", [])

                st.markdown(assistant_text)
                if tool_events:
                    with st.expander("🛠️ Chi tiết các tool đã gọi"):
                        st.json(tool_events)

                # Lưu lại lịch sử hội thoại
                st.session_state.chat_history.append({"role": "user", "content": user_prompt})
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})
                
                st.session_state.display_messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "tools": tool_events,
                })

            except Exception as err:
                st.error(f"Lỗi Provider / Agent: {err}")