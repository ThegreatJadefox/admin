import streamlit as st
import requests
import json



# Function to fetch reviews from GitHub
def get_reviews():
    url = "https://github.com/ThegreatJadefox/email-scraper/blob/main/support/reviews.json}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Streamlit UI
st.title("Customer Reviews Viewer")


if st.button("Refresh Reviews"):
    st.rerun()

reviews = get_reviews()

if reviews:
    for review in reviews:
        st.subheader(f"Review by {review['name']}")
        st.write(f"**Email:** {review['email']}")
        st.write(review['message'])
        st.markdown("---")
else:
    st.info("No reviews yet.")
