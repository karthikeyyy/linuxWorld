import streamlit as st
import os
import smtplib
import requests
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit app config
st.set_page_config(page_title="ChatGPT AI Automation Agent", layout="wide")

# Sidebar
st.sidebar.title("⚙️ AI Automation Agent")
st.sidebar.markdown("Built with **ChatGPT + Python + Streamlit**")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to call ChatGPT
def chat_with_gpt(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI automation agent."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# Function to send email
def send_email(to_email, subject, body, sender_email, sender_password):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Error: {e}"

# Function to search Google
def google_search(query):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key=YOUR_GOOGLE_API_KEY&cx=YOUR_SEARCH_ENGINE_ID"
        res = requests.get(url)
        data = res.json()
        results = [item["link"] for item in data.get("items", [])]
        return results[:5]
    except Exception as e:
        return [f"❌ Error: {e}"]

# Function to run Linux command
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

# Chat input
st.title("🤖 ChatGPT AI Automation Agent")
user_input = st.text_input("Enter your command or query:")

if st.button("Submit") and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    response = chat_with_gpt(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": response})

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Agent:** {msg['content']}")

# Automation Panel
st.subheader("⚡ Automation Tools")

with st.expander("📧 Send Email"):
    to_email = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message")
    sender_email = st.text_input("Your Email")
    sender_password = st.text_input("Your Email Password", type="password")
    if st.button("Send Email"):
        st.success(send_email(to_email, subject, body, sender_email, sender_password))

with st.expander("🔍 Google Search"):
    query = st.text_input("Search Query")
    if st.button("Search"):
        results = google_search(query)
        for r in results:
            st.write(r)

with st.expander("💻 Run Linux Command"):
    command = st.text_input("Enter Command")
    if st.button("Run"):
        output = run_command(command)
        st.text_area("Output", output, height=200)

# Footer
st.sidebar.info("🚀 Developed by Rohit Karadiya")
