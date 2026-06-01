# 📚 Book Recommendation System

A content-based book recommendation system that suggests similar books based on user selection. The application is built using Streamlit and uses precomputed similarity scores for fast and efficient recommendations.

## Features

* Book-to-book recommendations
* Interactive web interface using Streamlit
* Fast recommendations using similarity matrices

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit

## Project Structure

```text
.
├── app.py
├── books.pkl
├── popular.pkl
├── pt.pkl
├── similarity_scores.pkl
├── requirements.txt
├── README.md
└── book_recommender.ipynb
```

## Dataset

```
https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset?select=Users.csv
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mittalryan01/Book-Recommendation-System.git
```

### 2. Navigate to the project directory

```bash
cd Book-Recommendation-System
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit app using:

```bash
streamlit run app.py
```

The application will open automatically in your browser.


