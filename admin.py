import streamlit as st
import threading
import json
import os
from flask import Flask, request, jsonify

# --- Setup for the API server inside the viewer app ---
app = Flask(__name__)
DATA_FILE = "customer_review.json"

@app.route("/api/reviews", methods=["POST"])
def receive_review():
    """Receive a new review from the main app and save it."""
    review = request.get_json()
    # Load existing reviews or initialize empty list
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
    # Run Flask API on a specified port (e.g., 5001)
    app.run(port=5001)

# Start the API server in a background thread
api_thread = threading.Thread(target=run_api)
api_thread.daemon = True
api_thread.start()

# --- Streamlit code to display the reviews ---
st.title("Customer Reviews Viewer")

st.markdown("This app receives reviews from the main app via an API endpoint running in the background.")

# Provide a refresh button to re-read the JSON file
if st.button("Refresh Reviews"):
    st.experimental_rerun()

# Read and display reviews from the JSON file
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            reviews = json.load(f)
    except Exception as e:
        st.error(f"Error reading reviews: {e}")
        reviews = []
else:
    reviews = []

if reviews:
    for review in reviews:
        st.subheader(f"Review by {review.get('name', 'Anonymous')}")
        st.write(f"**Email:** {review.get('email', 'N/A')}")
        st.write(review.get('message', ''))
        st.markdown("---")
else:
    st.info("No reviews yet.")
