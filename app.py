import streamlit as st

st.set_page_config(page_title="成绩评级工具", page_icon="📊")
st.title("📊 成绩评级工具")
st.write("输入0~100分，自动判断等级")

score = st.number_input("请输入分数", min_value=0.0, max_value=100.0, value=60.0)

if score >= 90:
    level = "🏆 优秀"
elif score >= 80:
    level = "👍 良好"
elif score >= 60:
    level = "✅ 合格"
else:
    level = "❌ 不及格"

st.success(f"评级结果：{level}")
