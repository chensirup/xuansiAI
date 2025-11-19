import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit as st
import google.generativeai as genai
from PIL import Image
import re # 导入正则表达式库
# 移除 os 库，因为它现在已无用

# ==========================================
# 1. 页面配置与自定义样式
# ==========================================
st.set_page_config(
    page_title="玄师 · 掌中乾坤",
    page_icon="✋",
    layout="centered"
)

# 隐藏默认菜单，增加氛围CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #fcfbf9;
        color: #2c3e50;
    }
    .main-title {
        font-family: "Songti SC", "SimSun", serif; 
        text-align: center;
        color: #8b4513;
        font-size: 3em;
        margin-bottom: 20px;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        color: #5e4b35;
        font-size: 1.2em;
        margin-bottom: 30px;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 玄师的核心提示词 (System Prompt)
# ==========================================
XUANSHI_PROMPT = """
## 你的身份与世界观
你是一位名为「玄师」的手相宗师。你看的不是孤立的掌纹，而是掌纹背后那个独一无二的「生命剧本」。
你的所有分析都必须基于以下三大核心哲理：
『手为心印』 掌纹是思想、情绪和长期行为习惯的物理沉淀。
『掌为图谱』 八大丘位是天赋能量的源泉，主要纹路是能量流动的河道。
『相为启示』 你的最终目标是「唤醒」而非「预测」，为对方提供自我觉察和成长的智慧指引。

## 终极分析框架
请严格遵循以下五步法，对用户上传的手相图片进行解读：
〔第一步：观其气象〕整体印象，能量是内敛还是外放？
〔第二步：定其根基〕分析手型与手指，解读出厂设置。
〔第三步：察其流动〕逐一分析四大主线（生命、智慧、感情、事业）。
〔第四步：探其源泉〕评估主要丘位（金星丘等）。
〔第五步：归其大道〕核心故事、最大潜能、修行建议。

## 互动协议
- 风格：以宗师身份，语言古雅亲和。
- 格式：使用Markdown排版，重点加粗。
"""

# ==========================================
# 3. 侧边栏：专项问询选项（API Key已隐藏）
# ==========================================
with st.sidebar:
    st.header("🔮 专项问询")
    focus_area = st.radio(
        "除了综合解读，你还想重点看什么？",
        ["综合运势", "事业财运", "情感婚姻", "身心健康"]
    )
    st.markdown("---")
    st.markdown("💡 *本应用已由站长配置密钥，用户无需填写。*")

# ==========================================
# 4. 主界面逻辑
# ==========================================
st.markdown('<div class="main-title">✋ 手相宗师 · 玄师</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">“ 观掌中乾坤， 解生命剧本 ”</div>', unsafe_allow_html=True)

st.info("📸 请上传一张清晰的手掌照片（建议自然光，含手指手腕）。")

# 使用 label_visibility="hidden" 隐藏标签
uploaded_file = st.file_uploader("手相照片", type=["jpg", "jpeg", "png"], label_visibility="hidden")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # 使用 use_container_width=True
    st.image(image, caption="缘主手相", use_container_width=True)

    if st.button("请玄师阅卷", type="primary"):
        
        # <<< 关键修改：从 Streamlit Cloud UI 配置的 GEMINI_API_KEY 中读取 >>>
        api_key = st.secrets.get("GEMINI_API_KEY") 
        
        if not api_key:
            # <<< 修正提示：提示用户在 Streamlit Cloud 设置里配置密钥 >>>
            st.error("❌ 站长：密钥配置失败。请检查 Streamlit Cloud 的 Secrets 设置，确保配置了 'GEMINI_API_KEY'。")
        else:
            try:
                with st.spinner('玄师正在观气、定根、察流... 请稍候...'):
                    # 配置 API
                    genai.configure(api_key=api_key)
                    
                    # 使用 Pro 模型进行深度分析
                    model = genai.GenerativeModel('gemini-2.5-pro')
                    
                    # 构建最终提示词
                    final_prompt = XUANSHI_PROMPT
                    if focus_area != "综合运势":
                        final_prompt += f"\n\n【特别指令】用户希望重点分析：**{focus_area}**，请在【归其大道】后增加一个详细章节专门分析此项。"

                    # 发送请求
                    response = model.generate_content([final_prompt, image])
                    
                    # 展示结果
                    st.success("✅ 阅卷完毕")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    # 结束语
                    st.markdown("---")
                    st.markdown("<div style='text-align: center; color: gray;'>—— 命由己造，相由心生 ——</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ 天机连接失败，请检查密钥或网络：{e}")
