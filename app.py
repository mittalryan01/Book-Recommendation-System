import pickle
import streamlit as st
import numpy as np

st.set_page_config(
    page_title=" Book Recommender",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght=0,9..40,100..1000;1,9..40,100..1000&family=Space+Grotesk:wght=300..700&family=Roboto+Mono&display=swap');
    
    .stApp {
        background-color: #F9FAFB !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    button[data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #6B7280 !important; /* Secondary Gray */
        background-color: #F3F4F6 !important; /* Tertiary Light */
        padding: 8px 16px !important;
        border-radius: 12px 12px 0 0 !important;
        margin-right: 4px !important;
        border: 1px solid #E5E7EB !important;
        border-bottom: none !important;
        opacity: 0.85;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
        background-color: #3B82F6 !important; /* Primary Blue Accent */
        border-color: #3B82F6 !important;
        opacity: 1;
    }
    
    .micropost-display {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 30px;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: 0.02em;
        color: #111827;
        margin-top: 16px;
        margin-bottom: 24px;
    }
    
    .micropost-subhead {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 17px;
        font-weight: 600;
        line-height: 1.35;
        color: #374151;
        margin-bottom: 12px;
    }
    
    .micropost-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 16px;
        box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s, box-shadow 0.2s;
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    
    .micropost-card:hover {
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.06), 0px 1px 2px rgba(0, 0, 0, 0.04);
    }
    
    .micropost-card img {
        border-radius: 6px;
        max-width: 100%;
        height: 200px;
        object-fit: cover;
        margin-bottom: 8px;
    }
    
    .book-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 14px;
        font-weight: 700;
        line-height: 1.5;
        color: #111827;
        margin: 4px 0px 2px 0px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;  
        overflow: hidden;
    }
    
    .book-author {
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        color: #6B7280;
        margin-bottom: 6px;
    }
    
    .status-container {
        display: flex;
        gap: 4px;
        margin-top: auto;
    }
    
    .chip-success {
        background-color: #ECFDF5;
        color: #10B981;
        font-family: 'DM Sans', sans-serif;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        padding: 2px 8px;
        border-radius: 9999px;
        display: inline-block;
    }
    
    .chip-warning {
        background-color: #FFFBEB;
        color: #F59E0B;
        font-family: 'DM Sans', sans-serif;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        padding: 2px 8px;
        border-radius: 9999px;
        display: inline-block;
    }
    
    div.stButton > button {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 9999px !important; 
        padding: 6px 16px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        margin-top: 10px;
    }
    
    div.stButton > button:hover {
        background-color: #2563EB !important;
    }
    

    div[data-baseweb="select"] {
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    popular_df = pickle.load(open('popular.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    books = pickle.load(open('books.pkl', 'rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
    return popular_df, pt, books, similarity_scores

try:
    popular_df, pt, books, similarity_scores = load_data()
except FileNotFoundError:
    st.error("Data source files (.pkl) not found. Please ensure they exist in the root application directory.")
    st.stop()

available_books = sorted(list(pt.index))

tab1, tab2 = st.tabs(["🏠 Home", "🔍 Recommend Books"])

with tab1:
    st.markdown('<div class="micropost-display">Top 50 Books</div>', unsafe_allow_html=True)
    
    book_names = list(popular_df['Book-Title'].values)
    authors = list(popular_df['Book-Author'].values)
    images = list(popular_df['Image-URL-M'].values)
    votes = list(popular_df['num_ratings'].values)
    ratings = list(popular_df['avg_rating'].values)
    
    col_idx = 0
    cols = st.columns(4)
    
    for i in range(len(book_names)):
        with cols[col_idx]:
            st.markdown(f"""
                <div class="micropost-card">
                    <img src="{images[i]}" alt="{book_names[i]}">
                    <div class="book-title">{book_names[i]}</div>
                    <div class="book-author">by {authors[i]}</div>
                    <div class="status-container">
                        <span class="chip-success">★ {float(ratings[i]):.2f}</span>
                        <span class="chip-warning">👍 {votes[i]} votes</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        col_idx = (col_idx + 1) % 4

with tab2:
    st.markdown('<div class="micropost-display">Recommend Books</div>', unsafe_allow_html=True)
    
    st.markdown('<label style="font-family:\'DM Sans\'; font-size:12px; font-weight:600; color:#374151; margin-bottom:4px; display:block;">Select or Type a Book Title</label>', unsafe_allow_html=True)
    
    user_input = st.selectbox(
        label="Select or Type a Book Title",
        options=available_books,
        index=0,
        label_visibility="collapsed"
    )
    
    if st.button("Generate Recommendations"):
        try:
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
            
            rec_data = []
            for i in similar_items:
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                temp_df = temp_df.drop_duplicates('Book-Title')
                
                if not temp_df.empty:
                    item = [
                        temp_df['Book-Title'].values[0],
                        temp_df['Book-Author'].values[0],
                        temp_df['Image-URL-M'].values[0]
                    ]
                    rec_data.append(item)
            
            if rec_data:
                st.markdown('<div class="micropost-subhead" style="margin-top: 24px;">Recommended For You:</div>', unsafe_allow_html=True)
                rec_cols = st.columns(4)
                
                for idx, item in enumerate(rec_data):
                    with rec_cols[idx]:
                        st.markdown(f"""
                            <div class="micropost-card">
                                <img src="{item[2]}" alt="{item[0]}">
                                <div class="book-title">{item[0]}</div>
                                <div class="book-author">by {item[1]}</div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No matching variations found for your selection.")
                
        except Exception as e:
            st.error("An error occurred while tracking recommendations. Please try another title.")