import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


st.set_page_config(
    page_title="LinkedIn Post Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
        }
        .stSelectbox label {
            font-weight: 600 !important;
            color: #333333 !important;
        }
        .stButton button {
            background-color: #0A66C2;
            color: white;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            border: none;
        }
        .stButton button:hover {
            background-color: #004182;
        }
        .generated-post {
            background-color: white;
            padding: 1rem;
            border-left: 5px solid #0A66C2;
            border-radius: 6px;
            font-size: 16px;
            color: #212529;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)


def main():
    st.title("LinkedIn Post Generator")


    st.markdown('<div class="main">', unsafe_allow_html=True)

    fs = FewShotPosts()
    tags = fs.get_tags()

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=["Short", "Medium", "Long"])

    with col3:
        selected_language = st.selectbox("Language", options=["English"])

    st.markdown("<br>", unsafe_allow_html=True)

    generate_col = st.columns([3, 1, 3])[1]
    with generate_col:
        generate = st.button("Generate Post")

    st.markdown("<br>", unsafe_allow_html=True)

    if generate:
        post = generate_post(selected_length, selected_language, selected_tag)
        st.markdown("#### Generated Post")
        st.markdown(f"<div class='generated-post'>{post}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
