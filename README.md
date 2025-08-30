# 📰 AI Article Summarizer

An interactive Streamlit app that summarizes long-form text from pasted input or fetched web articles using a distilled BART model, and then suggests simple related topics based on the generated summary.

## ✨ Features
- 📋 Paste text or 🌐 enter a URL; the app fetches paragraphs from the page and prepares the text for summarization.  
- ⚡ Fast, news-style summarization powered by `sshleifer/distilbart-cnn-12-6` from Hugging Face Transformers.  
- 🔗 Lightweight “Related Articles” suggestions derived from early summary keywords for quick exploration.  
- 🎨 Clean Streamlit UI with session state so fetched or edited text persists across interactions.  

## 🚀 Live app
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://article-summarization-tarunsingh1803.streamlit.app/)

## 🛠️ Tech stack
- 🖥️ **Streamlit** — web UI framework for interactive app building.  
- 🤗 **Transformers (Hugging Face)** — summarization model `sshleifer/distilbart-cnn-12-6` using `BartTokenizer` + `BartForConditionalGeneration`.  
- 🔥 **PyTorch** — inference backend for the model.  
- 🌐 **Requests + BeautifulSoup4** — HTTP fetching and HTML parsing for articles.  
- 📊 **scikit-learn, ROUGE, YAKE, NLTK** — used in the exploratory notebook for keyword extraction, evaluation, and experimentation.  

## 📂 Project structure
- 📄 `app.py` — Streamlit app: model loading, URL fetching, text input, summarization, and related items UI.  
- 📓 `article_web.ipynb` — Exploration: model init, scraping helper, keyword extraction, TF-IDF related-article matching, ROUGE, and local model save.  
- 📑 `requirements.txt` — Pinned dependencies for reproducible installs.  

## ⚙️ Getting started (local)
1️⃣  Environment setup
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2️⃣ Run
```bash
streamlit run app.py
```

3️⃣ Use
- Select “✍️ Paste Text” to input content or “🌐 Enter URL” to fetch an article, then click “✨ Generate Summary.”

## 🌍 Deployment (Streamlit Community Cloud)
- ⬆️ Push this repo to GitHub with `app.py` at the root and `requirements.txt` included.
- 🔗 Go to [share.streamlit.io](https://share.streamlit.io), click “Create app,” choose the repo/branch, and set `app.py` as the entrypoint.
- 🏷️ Optional: Choose a custom subdomain during setup, then update the README badge link to the final URL.

## ⚠️ Notes and limitations
- ⚡ The distilBART model trades some quality for speed; performance is strongest on news-style content.
- 🕸️ Basic paragraph scraping is used; complex or script-heavy sites may yield limited or noisy text extraction.

## 📜 License and attributions
- 📖 Respect licenses for Hugging Face Transformers and the `sshleifer/distilbart-cnn-12-6` model; consult their model card and library documentation for terms.


