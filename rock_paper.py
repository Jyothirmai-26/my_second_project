import random
from datetime import datetime
import streamlit as st


# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------

st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="🎮",
    layout="wide"
)


# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("🎮 Jyothirmai's Rock Paper Scissors Game")
st.caption("Choose your move and challenge the computer!")


# -------------------------------------------------
# GAME DATA
# -------------------------------------------------

CHOICES = ["Rock", "Paper", "Scissors"]

WIN_RULES = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper"
}

TARGETS = {
    "Best of 3": 2,
    "Best of 5": 3,
    "Best of 7": 4,
    "Unlimited": None
}


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

defaults = {
    "user_score": 0,
    "computer_score": 0,
    "draws": 0,
    "games": 0,
    "streak": 0,
    "best_streak": 0,
    "history": [],
    "finished": False,
    "last_user": "",
    "last_computer": "",
    "result": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------

def get_result(user_choice, computer_choice):

    if user_choice == computer_choice:
        return "Draw"

    if WIN_RULES[user_choice] == computer_choice:
        return "Win"

    return "Loss"


def reset_game():

    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.draws = 0
    st.session_state.games = 0
    st.session_state.streak = 0
    st.session_state.history = []
    st.session_state.finished = False
    st.session_state.last_user = ""
    st.session_state.last_computer = ""
    st.session_state.result = ""


def play_round(user_choice):

    computer_choice = random.choice(CHOICES)

    result = get_result(user_choice, computer_choice)

    st.session_state.games += 1
    st.session_state.last_user = user_choice
    st.session_state.last_computer = computer_choice
    st.session_state.result = result

    if result == "Win":

        st.session_state.user_score += 1
        st.session_state.streak += 1

        if st.session_state.streak > st.session_state.best_streak:
            st.session_state.best_streak = st.session_state.streak

    elif result == "Loss":

        st.session_state.computer_score += 1
        st.session_state.streak = 0

    else:

        st.session_state.draws += 1

    st.session_state.history.append(
        {
            "Round": st.session_state.games,
            "You": user_choice,
            "Computer": computer_choice,
            "Result": result,
            "Time": datetime.now().strftime("%H:%M:%S")
        }
    )


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.header("⚙️ Game Settings")

    player_name = st.text_input(
        "Player Name",
        value="Jyothirmai"
    )

    match_mode = st.selectbox(
        "Match Mode",
        list(TARGETS.keys())
    )

    show_reactions = st.checkbox(
        "Show reactions",
        value=True
    )

    show_history = st.checkbox(
        "Show game history",
        value=True
    )

    st.divider()

    st.subheader("📖 Quick Rules")

    st.write("✊ Rock beats Scissors")
    st.write("📄 Paper beats Rock")
    st.write("✂️ Scissors beats Paper")

    st.divider()

    if st.button(
        "🔄 Reset Current Match",
        use_container_width=True
    ):
        reset_game()
        st.rerun()

    if st.button(
        "🧹 Clear History",
        use_container_width=True
    ):
        st.session_state.history = []
        st.rerun()


# -------------------------------------------------
# MATCH TARGET
# -------------------------------------------------

target = TARGETS[match_mode]

if target is not None:

    if (
        st.session_state.user_score >= target
        or st.session_state.computer_score >= target
    ):
        st.session_state.finished = True


# -------------------------------------------------
# PLAYER INFORMATION
# -------------------------------------------------

st.write(f"### 👋 Welcome, {player_name}!")
st.write(f"**Match Mode:** {match_mode}")

st.divider()


# -------------------------------------------------
# SCORE
# -------------------------------------------------

st.subheader("📊 Score")

score1, score2, score3, score4, score5 = st.columns(5)

with score1:
    st.metric(
        "🏆 Your Score",
        st.session_state.user_score
    )

with score2:
    st.metric(
        "🤖 Computer",
        st.session_state.computer_score
    )

with score3:
    st.metric(
        "🤝 Draws",
        st.session_state.draws
    )

with score4:
    st.metric(
        "🔥 Current Streak",
        st.session_state.streak
    )

with score5:
    st.metric(
        "🥇 Best Streak",
        st.session_state.best_streak
    )


st.divider()


# -------------------------------------------------
# MAIN GAME AREA
# -------------------------------------------------

game_col, info_col = st.columns([1.5, 1])


# -------------------------------------------------
# GAME
# -------------------------------------------------

with game_col:

    st.subheader("🎮 Choose Your Move")

    st.write("Select one option below:")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("✊ Rock")

        rock_button = st.button(
            "Play Rock",
            use_container_width=True,
            disabled=st.session_state.finished
        )

    with col2:

        st.subheader("📄 Paper")

        paper_button = st.button(
            "Play Paper",
            use_container_width=True,
            disabled=st.session_state.finished
        )

    with col3:

        st.subheader("✂️ Scissors")

        scissors_button = st.button(
            "Play Scissors",
            use_container_width=True,
            disabled=st.session_state.finished
        )


    # -------------------------------------------------
    # BUTTON ACTION
    # -------------------------------------------------

    selected_choice = None

    if rock_button:
        selected_choice = "Rock"

    elif paper_button:
        selected_choice = "Paper"

    elif scissors_button:
        selected_choice = "Scissors"


    if selected_choice is not None:

        play_round(selected_choice)

        st.rerun()


    # -------------------------------------------------
    # RESULT
    # -------------------------------------------------

    if st.session_state.result:

        st.divider()

        st.subheader("🎯 Round Result")

        st.write(
            f"**You:** {st.session_state.last_user}"
        )

        st.write(
            f"**Computer:** {st.session_state.last_computer}"
        )

        if st.session_state.result == "Win":

            st.success("🎉 You won this round!")

            if show_reactions:
                st.balloons()

        elif st.session_state.result == "Loss":

            st.error("😔 Computer won this round.")

        else:

            st.info("🤝 It's a draw!")

    else:

        st.info(
            "Choose Rock, Paper, or Scissors to start the game."
        )


# -------------------------------------------------
# PERFORMANCE AREA
# -------------------------------------------------

with info_col:

    st.subheader("📈 Performance")

    if st.session_state.games > 0:

        win_percentage = (
            st.session_state.user_score
            / st.session_state.games
        ) * 100

        st.metric(
            "Games Played",
            st.session_state.games
        )

        st.metric(
            "Win Percentage",
            f"{win_percentage:.1f}%"
        )

    else:

        st.write("No games played yet.")

    st.divider()

    st.subheader("🏅 Achievements")

    if st.session_state.best_streak >= 3:
        st.success("🔥 3 Win Streak!")

    if st.session_state.best_streak >= 5:
        st.success("🏆 5 Win Streak!")

    if st.session_state.user_score >= 10:
        st.success("⭐ 10 Wins!")

    if st.session_state.games >= 20:
        st.success("🎮 20 Games Played!")

    if st.session_state.best_streak < 3:
        st.write("Keep playing to unlock achievements!")


# -------------------------------------------------
# MATCH PROGRESS
# -------------------------------------------------

st.divider()

st.subheader("🥊 Match Progress")

if target is not None:

    current_score = max(
        st.session_state.user_score,
        st.session_state.computer_score
    )

    progress = min(
        current_score / target,
        1.0
    )

    st.progress(progress)

    st.write(
        f"First player to reach **{target} wins**."
    )

    if st.session_state.user_score >= target:

        st.success("🏆 Congratulations! You won the match!")

    elif st.session_state.computer_score >= target:

        st.error("🤖 Computer won the match!")

else:

    st.progress(0)

    st.write("Unlimited mode: play as many rounds as you want.")


# -------------------------------------------------
# NEW MATCH
# -------------------------------------------------

if st.session_state.finished:

    st.divider()

    if st.button(
        "🎮 Start New Match",
        use_container_width=True
    ):

        reset_game()
        st.rerun()


# -------------------------------------------------
# GAME HISTORY
# -------------------------------------------------

if show_history and st.session_state.history:

    st.divider()

    st.subheader("📝 Recent Game History")

    st.dataframe(
        st.session_state.history,
        use_container_width=True,
        hide_index=True
    )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "🎮 Rock Paper Scissors | Built with Streamlit"
)