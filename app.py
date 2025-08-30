import streamlit as st
from transformers import BartTokenizer, BartForConditionalGeneration
import requests
from bs4 import BeautifulSoup

# ----------------------------
# Load saved model + tokenizer
# ----------------------------
@st.cache_resource
def load_model():
    model_name = "sshleifer/distilbart-cnn-12-6"   # smaller + faster
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()
# ----------------------------
# Summarization function
# ----------------------------
def generate_summary(text, max_len=150):
    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        max_length=max_len,
        min_length=30,
        early_stopping=True,
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# ----------------------------
# Fetch article from URL
# ----------------------------
def fetch_article_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        article_text = " ".join(paragraphs).strip()
        if not article_text:
            return None, "No article paragraphs found on this page."
        return article_text, None
    except Exception as e:
        return None, f"Error fetching article: {e}"

# ----------------------------
# Related articles mock DB
# ----------------------------
articles_database = [
    {"title": "Global Trends in Electric Vehicles"},
    {"title": "How Renewable Energy Impacts Economy"},
    {"title": "AI Transforming the Future of Work"},
    {"title": "Climate Change and Global Policy Shifts"},
]

def find_related_articles(summary, database):
    related = []
    for article in database:
        if any(word.lower() in article["title"].lower() for word in summary.split()[:10]):
            related.append(article)
    return related if related else database[:2]

# ----------------------------
# Session state init
# ----------------------------
if "article_text" not in st.session_state:
    st.session_state["article_text"] = ""  # will store the editable text
if "fetch_msg" not in st.session_state:
    st.session_state["fetch_msg"] = ""  # optional message about last fetch

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Article Summarizer", page_icon="📰", layout="wide")

st.title("📰 AI Article Summarizer")
st.markdown("Choose input type: paste text or provide a URL to generate a concise summary with related topics!")

input_type = st.radio("Select Input Type:", ("✍️ Paste Text", "🌐 Enter URL"), index=0)

# --- URL branch ---
if input_type == "🌐 Enter URL":
    url = st.text_input("Enter article URL:", key="url_input")
    if st.button("📥 Fetch Article"):
        if url.strip():
            fetched, err = fetch_article_from_url(url)
            if err:
                st.session_state["fetch_msg"] = err
                st.error(err)
            else:
                st.session_state["article_text"] = fetched  # store fetched article in session_state
                st.session_state["fetch_msg"] = "✅ Article fetched successfully!"
                st.success(st.session_state["fetch_msg"])
        else:
            st.warning("⚠️ Please enter a valid URL.")

# --- Paste text branch ---
if input_type == "✍️ Paste Text":
    # show an editable text area (value is from session_state so it persists across reruns)
    st.text_area("Paste your article here:", value=st.session_state["article_text"], height=250, key="article_text")

else:
    # After fetching we still want the user to be able to edit or preview the article.
    st.text_area("Fetched Article (editable):", value=st.session_state["article_text"], height=250, key="article_text")

# ----------------------------
# Summarize
# ----------------------------
if st.button("✨ Generate Summary"):
    article = st.session_state.get("article_text", "")
    if article and article.strip():
        with st.spinner("Summarizing..."):
            summary = generate_summary(article)
        st.subheader("📌 Summary")
        st.success(summary)

        related = find_related_articles(summary, articles_database)
        st.subheader("🔗 Related Articles")
        for idx, art in enumerate(related, start=1):
            st.write(f"**{idx}. {art['title']}**")
    else:
        st.warning("⚠️ Please provide text or fetch an article first.")


