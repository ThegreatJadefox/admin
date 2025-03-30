import streamlit as st
import threading
import json
import os
from flask import Flask, request, jsonify

# --- Setup for the API server inside the viewer app ---
# This app is deployed at https://scraperreviews.streamlit.app
app = Flask(__name__)
DATA_FILE = "customer_review.json"

@app.route("/api/reviews", methods=["POST"])
def receive_review():
    """Receive a new review from the main app and save it."""
    review = request.get_json()
    # Load existing reviews or initialize an empty list
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                reviews = json.load(f)
        except json.JSONDecodeError:
            reviews = []
    else:
        reviews = []
    
    # Append the new review and save back to the file
    reviews.append(review)
    with open(DATA_FILE, "w") as f:
        json.dump(reviews, f, indent=4)
    return jsonify({"status": "success"}), 200

def run_api():
    # Run the Flask API on a specified port (e.g., 5001)
    app.run(port=55555)

# Start the API server in a background thread
api_thread = threading.Thread(target=run_api)
api_thread.daemon = True
api_thread.start()

# --- Streamlit code to display the reviews ---
st.title("Customer Reviews Viewer")
st.markdown("This app receives reviews via an API endpoint and displays them here.")

# Initialize a session state counter to force data reloads
if 'refresh_counter' not in st.session_state:
    st.session_state.refresh_counter = 0

if st.button("Refresh Reviews"):
    st.session_state.refresh_counter += 1

# Use a caching function that depends on the refresh counter.
@st.cache_data(ttl=10)
def load_reviews(refresh):
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error reading reviews: {e}")
            return []
    else:
        return []

reviews = load_reviews(st.session_state.refresh_counter)

if reviews:
    for review in reviews:
        st.subheader(f"Review by {review.get('name', 'Anonymous')}")
        st.write(f"**Email:** {review.get('email', 'N/A')}")
        st.write(review.get('message', ''))
        st.markdown("---")
else:
    st.info("No reviews yet.")
