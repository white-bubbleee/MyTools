import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="智能评分系统", layout="centered")

st.title("🎯 智能评分与排序系统")

# --- Step 1: 输入指标 ---
st.header("① 设置评分指标和权重")
criteria_input = st.text_input("请输入所有指标名称（用逗号分隔）", "薪资,稳定性,发展性,工作地点")
criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]

weights = []
cols = st.columns(len(criteria))
for i, c in enumerate(criteria):
    with cols[i]:
        w = st.number_input(f"{c} 权重", value=1.0, step=0.1, min_value=0.0)
        weights.append(w)

# 归一化权重
total_w = sum(weights)
if total_w != 0:
    weights = [w / total_w for w in weights]

# --- Step 2: 输入对象与得分 ---
st.header("② 输入各对象得分")
num_items = st.number_input("要评估的对象数量", min_value=1, step=1, value=3)

data = []
for i in range(int(num_items)):
    st.subheader(f"对象 {i+1}")
    name = st.text_input(f"请输入第 {i+1} 个对象名称", key=f"name_{i}")
    scores = []
    cols = st.columns(len(criteria))
    for j, c in enumerate(criteria):
        with cols[j]:
            s = st.number_input(f"{c} 得分（0~10）", min_value=0.0, max_value=10.0, step=0.1, key=f"{i}_{c}")
            scores.append(s)
    if name:
        data.append([name] + scores)

# --- Step 3: 计算总分并显示 ---
if st.button("计算结果"):
    if not data:
        st.warning("请至少输入一个对象及其得分。")
    else:
        df = pd.DataFrame(data, columns=["对象"] + criteria)
        df["总分"] = df[criteria].apply(lambda row: sum(row[i] * weights[i] for i in range(len(criteria))), axis=1)
        df = df.sort_values(by="总分", ascending=False).reset_index(drop=True)

        st.success("计算完成 ✅")
        st.write("### 排名结果：")
        st.dataframe(df)

        # --- 绘图显示 ---
        st.write("### 排名图：")
        fig, ax = plt.subplots()
        ax.barh(df["对象"], df["总分"], color="skyblue")
        ax.invert_yaxis()
        ax.set_xlabel("得分")
        ax.set_title("总分排名")
        st.pyplot(fig)
