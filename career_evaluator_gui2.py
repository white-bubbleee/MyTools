import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# ======================
# 🔧 全局配置
# ======================
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体
plt.rcParams['axes.unicode_minus'] = False    # 修复负号乱码

st.set_page_config(page_title="智能评分系统", layout="centered")
st.title("🎯 智能评分与排序系统")

# ======================
# 🧩 函数定义
# ======================

def normalize_weights(weights):
    """权重归一化"""
    total = sum(weights)
    return [w / total for w in weights] if total != 0 else weights


def calculate_scores(data, criteria, weights):
    """计算每个对象的加权总分"""
    df = pd.DataFrame(data, columns=["对象"] + criteria)
    df["总分"] = df[criteria].apply(lambda row: sum(row[i] * weights[i] for i in range(len(criteria))), axis=1)
    return df.sort_values(by="总分", ascending=False).reset_index(drop=True)


def draw_chart(df):
    """绘制条形图"""
    df_plot = df.sort_values("总分")
    fig, ax = plt.subplots(figsize=(7, max(4, len(df_plot) * 0.6)))
    bars = ax.barh(df_plot["对象"], df_plot["总分"], color="#5DADE2", alpha=0.85, height=0.45)

    ax.set_xlabel("总分", fontsize=13)
    ax.set_ylabel("对象", fontsize=13)
    ax.set_title("职业评分排名", fontsize=16, weight="bold", pad=10)
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.05, bar.get_y() + bar.get_height()/2,
                f"{width:.2f}", va="center", fontsize=11)

    st.pyplot(fig)


def export_excel(df):
    """导出结果为 Excel 文件"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="评分结果")
        workbook = writer.book
        worksheet = writer.sheets["评分结果"]
        # 设置列宽
        worksheet.set_column("A:A", 15)
        worksheet.set_column("B:Z", 12)
    output.seek(0)
    return output

# ======================
# ⚙️ Step 1: 输入指标
# ======================
st.header("① 设置评分指标和权重")
criteria_input = st.text_input("请输入所有指标名称（用逗号分隔）", "薪资,稳定性,发展性,工作地点")
criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]

weights = []
cols = st.columns(len(criteria))
for i, c in enumerate(criteria):
    with cols[i]:
        w = st.number_input(f"{c} 权重", value=1.0, step=0.1, min_value=0.0)
        weights.append(w)

weights = normalize_weights(weights)

# ======================
# ⚙️ Step 2: 输入对象与得分
# ======================
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

# ======================
# 📊 Step 3: 计算与显示
# ======================
if st.button("🚀 计算结果"):
    if not data:
        st.warning("请至少输入一个对象及其得分。")
    else:
        df = calculate_scores(data, criteria, weights)

        st.success("✅ 计算完成！")
        st.write("### 📋 排名结果：")
        st.dataframe(df, use_container_width=True)

        # 绘制图表
        st.write("### 📊 排名图：")
        draw_chart(df)

        # ======================
        # 💾 Step 4: 导出功能
        # ======================
        st.write("### 💾 导出结果：")
        excel_file = export_excel(df)
        st.download_button(
            label="⬇️ 下载结果表（Excel格式）",
            data=excel_file,
            file_name="职业评分结果.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
