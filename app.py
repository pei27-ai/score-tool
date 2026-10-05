import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("成绩评级工具")
st.subheader("输入分数，自动评级")
score = st.number_input("输入考试分数", min_value=0, max_value=100, step=1)
if st.button("计算评级"):
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "E"
    st.success(f"你的评级：{grade}")


st.divider()
st.header("🔍网页关键词搜索工具")
keyword = st.text_input("在这里输入中文关键词搜索", value="python教程")
search_btn = st.button("开始搜索并抓取结果")

if search_btn and keyword.strip():
    results = []
    # 模拟浏览器请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # 百度搜索
        url = f"https://www.baidu.com/s?wd={keyword}"
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("div.result-op")
        for item in items:
            title_tag = item.select_one("h3 a")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag["href"]
            results.append({"标题": title, "链接": link})

        st.success(f"搜索完成！关键词【{keyword}】，抓到 {len(results)} 条结果")
        st.subheader("搜索结果（点击标题打开网页）")
        for row in results:
            st.markdown(f"[{row['标题']}]({row['链接']})")

        # 导出CSV
        if results:
            df = pd.DataFrame(results)
            csv_data = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="下载本次搜索结果CSV",
                data=csv_data,
                file_name="search_result.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"请求出错：{str(e)}")

st.warning("本程序仅用于编程学习测试，不要高频批量爬取搜索引擎，遵守网络安全相关法律法规！")
