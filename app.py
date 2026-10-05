import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

st.set_page_config(page_title="成绩评级工具", page_icon="📊")
st.title("📊 成绩评级工具")
st.write("输入0~100分，自动判断等级")

# ========== 原来的分数评价代码 ==========
score = st.number_input("请输入分数", min_value=0, max_value=100, value=60)
if score >= 90:
    level = "🏆 优秀"
elif score >= 80:
    level = "👍 良好"
elif score >= 70:
    level = "📗 中等"
elif score >= 60:
    level = "✅ 合格"
else:
    level = "❌ 不及格"

if st.button("评级"):
    st.success(f"评级结果：{level}")

# ========== 新增：关键词搜索爬虫模块 ==========
st.divider()
st.header("🔍 网页关键词搜索工具")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

keyword = st.text_input("在这里输入中文关键词搜索", value="python教程")

if st.button("开始搜索并抓取结果"):
    try:
        with st.spinner("正在访问搜索引擎，抓取结果..."):
            search_url = f"https://www.baidu.com/s?wd={keyword}"
            resp = requests.get(search_url, headers=headers, timeout=10)
            resp.raise_for_status()
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "html.parser")

            result_list = []
            items = soup.select("div.result-op, div[class*='result']")
            for item in items:
                title_tag = item.find("h3")
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)
                link_tag = title_tag.find("a")
                link = link_tag.get("href") if link_tag else ""
                if title and link:
                    result_list.append({"标题": title, "网页链接": link})

        st.success(f"搜索完成！关键词【{keyword}】，抓到 {len(result_list)} 条结果")

        st.subheader("搜索结果（点击标题打开网页）")
        for row in result_list:
            st.markdown(f"- [{row['标题']}]({row['网页链接']})", unsafe_allow_html=False)

        # 下载CSV
        df = pd.DataFrame(result_list)
        csv_data = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 下载本次搜索结果CSV",
            data=csv_data,
            file_name=f"{keyword}_搜索结果.csv",
            mime="text/csv"
        )

    except Exception as err:
        st.error(f"搜索失败：{err}")

st.warning("⚠️本程序仅用于编程学习测试，不要高频批量爬取搜索引擎，遵守网络安全相关法律法规！")
