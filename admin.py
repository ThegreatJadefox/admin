import streamlit as st
import requests
import json

# GitHub Configuration
GITHUB_USER = "ThegreatJadefox"
GITHUB_REPO = "review-storage"
GITHUB_FILE = "reviews.json"

# Function to fetch reviews from GitHub
def get_reviews():
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/{GITHUB_FILE}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Streamlit UI
st.title("Customer Reviews Viewer")
st.markdown("Reviews are stored in a GitHub JSON file.")

if st.button("Refresh Reviews"):
    st.experimental_rerun()

reviews = get_reviews()

if reviews:
    for review in reviews:
        st.subheader(f"Review by {review['name']}")
        st.write(f"**Email:** {review['email']}")
        st.write(review['message'])
        st.markdown("---")
else:
    st.info("No reviews yet.")
