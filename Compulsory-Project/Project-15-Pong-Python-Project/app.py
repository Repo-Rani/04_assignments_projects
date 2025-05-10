import streamlit as st
import random

st.set_page_config(page_title="Enhanced Pong Game", layout="wide")

BOARD_WIDTH = 20
BOARD_HEIGHT = 15
PADDLE_HEIGHT = 3
INITIAL_LIVES = 3

defaults = {
    'ball_x': BOARD_WIDTH // 2,
    'ball_y': BOARD_HEIGHT // 2,
    'ball_dx': -1,
    'ball_dy': random.choice([-1, 1]),
    'paddle_y': BOARD_HEIGHT // 2 - PADDLE_HEIGHT // 2,
    'ai_paddle_y': BOARD_HEIGHT // 2 - PADDLE_HEIGHT // 2,
    'score': 0,
    'lives': INITIAL_LIVES,
    'difficulty': 'Easy',
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

difficulty_speed = {
    'Easy': 1,
    'Medium': 2,
    'Hard': 3
}

with st.sidebar:
    st.title("🎮 Game Settings")
    st.session_state['difficulty'] = st.selectbox("Select Difficulty", ['Easy', 'Medium', 'Hard'])

col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    st.markdown("<h2 style='text-align: center;'>🕹️ Pong Game</h2>", unsafe_allow_html=True)

    status = f"""
    <div style='text-align: center; font-size: 20px; margin-bottom: 15px;'>
        <span style='color: green;'>🏆 Score: {st.session_state.score}</span> &nbsp;|&nbsp;
        <span style='color: red;'>❤️ Lives: {st.session_state.lives}</span> &nbsp;|&nbsp;
        <span style='color: orange;'>⚙️ Difficulty: {st.session_state.difficulty}</span>
    </div>
    """
    st.markdown(status, unsafe_allow_html=True)

    st.markdown(
        """
        <div style='text-align: center; margin-top: 40px;'>
            <h3 style='margin-bottom: 20px;'>🎮 Paddle Control</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    col2_left, col2_right = st.columns([1, 1])

    with col2_left:
        if st.button("⬆️ Up"):
            st.session_state.paddle_y = max(0, st.session_state.paddle_y - 1)

    with col2_right:
        if st.button("⬇️ Down"):
            st.session_state.paddle_y = min(BOARD_HEIGHT - PADDLE_HEIGHT, st.session_state.paddle_y + 1)

if st.session_state.ball_y > st.session_state.ai_paddle_y + 1:
    st.session_state.ai_paddle_y = min(BOARD_HEIGHT - PADDLE_HEIGHT, st.session_state.ai_paddle_y + 1)
elif st.session_state.ball_y < st.session_state.ai_paddle_y:
    st.session_state.ai_paddle_y = max(0, st.session_state.ai_paddle_y - 1)


for _ in range(difficulty_speed[st.session_state['difficulty']]):
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy

    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= BOARD_HEIGHT - 1:
        st.session_state.ball_dy *= -1

    if st.session_state.ball_x == 1:
        if st.session_state.paddle_y <= st.session_state.ball_y < st.session_state.paddle_y + PADDLE_HEIGHT:
            st.session_state.ball_dx *= -1
            st.session_state.score += 1
        else:
            st.session_state.lives -= 1
            if st.session_state.lives <= 0:
                st.error(f"💀 Game Over! Final Score: {st.session_state.score}")
                if st.button("🔁 Restart"):
                    for k in defaults.keys():
                        st.session_state[k] = defaults[k]
                st.stop()
            else:
                st.warning(f"❌ Missed! Lives Left: {st.session_state.lives}")
                st.session_state.ball_x = BOARD_WIDTH // 2
                st.session_state.ball_y = BOARD_HEIGHT // 2
                st.session_state.ball_dx = -1
                st.session_state.ball_dy = random.choice([-1, 1])
                break


    if st.session_state.ball_x == BOARD_WIDTH - 2:
        if st.session_state.ai_paddle_y <= st.session_state.ball_y < st.session_state.ai_paddle_y + PADDLE_HEIGHT:
            st.session_state.ball_dx *= -1

st.session_state.ball_x = max(0, min(st.session_state.ball_x, BOARD_WIDTH - 1))
st.session_state.ball_y = max(0, min(st.session_state.ball_y, BOARD_HEIGHT - 1))


board = [["🟦" for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


for i in range(PADDLE_HEIGHT):
    if 0 <= st.session_state.paddle_y + i < BOARD_HEIGHT:
        board[st.session_state.paddle_y + i][0] = "🟥"

for i in range(PADDLE_HEIGHT):
    if 0 <= st.session_state.ai_paddle_y + i < BOARD_HEIGHT:
        board[st.session_state.ai_paddle_y + i][BOARD_WIDTH - 1] = "🟩"


if 0 <= st.session_state.ball_y < BOARD_HEIGHT and 0 <= st.session_state.ball_x < BOARD_WIDTH:
    board[st.session_state.ball_y][st.session_state.ball_x] = "🔵"

with col2:
    board_html = "<div style='font-size: 24px; font-family: monospace; text-align: center;'>"
    for row in board:
        board_html += "".join(row) + "<br>"
    board_html += "</div>"

    st.markdown(board_html, unsafe_allow_html=True)