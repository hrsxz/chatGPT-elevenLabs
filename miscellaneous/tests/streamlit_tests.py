import streamlit as st

# 创建两个列，分配空间比例为3:1
col1, col2 = st.columns([3, 1])

# 在第一列中使用placeholder1
placeholder1 = col1.empty()
with placeholder1:
    st.markdown("## This is column 1")

# 在第二列中，直接添加内容到第一行和第二行
with col2:
    st.markdown("### This is column 2, row 1")
    # 添加第二行内容
    st.markdown("### This is column 2, row 2")

# 如果需要，你也可以在第二列的特定位置创建空的占位符以后再填充内容
placeholder2_row1 = col2.empty()
placeholder2_row2 = col2.empty()

# 填充第二列的第一个占位符（第一行）
with placeholder2_row1:
    st.write("This is the new content for column 2, row 1")

# 填充第二列的第二个占位符（第二行）
with placeholder2_row2:
    st.write("This is the new content for column 2, row 2")
