import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

# 페이지 설정
st.set_page_config(page_title="건축 벽돌 시뮬레이터", layout="wide")

st.title("🧱 스마트 벽돌 쌓기 & 물량 산출기")
st.sidebar.header("설계 파라미터 조절")

# 사이드바 컨트롤 UI
rows = st.sidebar.slider("전체 층수", 1, 50, 15)
cols = st.sidebar.slider("가로 벽돌 개수", 1, 50, 15)

st.sidebar.subheader("🪟 창문 설정")
win_y = st.sidebar.number_input("창문 시작 높이(층)", 0, rows-1, 5)
win_x = st.sidebar.number_input("창문 시작 위치(열)", 0, cols-1, 5)
win_h = st.sidebar.number_input("창문 세로 크기", 1, 10, 5)
win_w = st.sidebar.number_input("창문 가로 크기", 1, 10, 4)

st.sidebar.subheader("💰 비용 설정")
price_per_brick = st.sidebar.number_input("벽돌 단가 (원)", 0, 5000, 500)

def draw_wall():
    brick_width = 2
    brick_height = 1
    brick_count = 0
    colors = ['#A52A2A', '#8B4513', '#B22222', '#CD5C5C', '#A0522D']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    win_end_y = win_y + win_h - 1
    win_end_x = win_x + win_w - 1

    for row in range(rows):
        offset = (row % 2) * (brick_width / 2)
        for col in range(cols):
            # 창문 영역 체크
            if (win_y <= row <= win_end_y) and (win_x <= col <= win_end_x):
                continue
            
            x = col * brick_width + offset
            y = row * brick_height
            
            rect = patches.Rectangle(
                (x, y), brick_width, brick_height, 
                linewidth=0.5, edgecolor='#333333', 
                facecolor=random.choice(colors),
                alpha=0.9
            )
            ax.add_patch(rect)
            brick_count += 1

    # 그래프 설정
    plt.xlim(-1, cols * brick_width + 2)
    plt.ylim(-1, rows * brick_height + 1)
    plt.gca().set_aspect('equal')
    plt.axis('off')
    
    return fig, brick_count

# 결과 출력
fig, count = draw_wall()
total_cost = count * price_per_brick

col1, col2, col3 = st.columns(3)
col1.metric("총 벽돌 수", f"{count} EA")
col2.metric("벽면 크기", f"{cols*2}m x {rows}m")
col3.metric("예상 재료비", f"{total_cost:,} 원")

st.pyplot(fig)
