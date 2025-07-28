import streamlit as st
from dotenv import load_dotenv
import os
import yagmail
from twilio.rest import Client
import requests
import tweepy
from instagrapi import Client as InstaClient

load_dotenv()

st.set_page_config(page_title="All-in-One Communication App", layout="wide")
st.title("📬 Multi-Platform Communication App")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📧 Email", "📱 SMS & Call", "💼 LinkedIn", "🐦 Twitter",
    "📘 Facebook", "📸 Instagram", "🟢 WhatsApp", "🧩 Combine All"
])

# -------- Email --------
with tab1:
    st.header("📧 Send Email")
    email_to = st.text_input("To Email")
    email_subject = st.text_input("Subject")
    email_body = st.text_area("Message")
    if st.button("Send Email"):
        try:
            yag = yagmail.SMTP(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            yag.send(to=email_to, subject=email_subject, contents=email_body)
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Failed: {e}")

# -------- SMS and Call --------
with tab2:
    st.header("📱 Send SMS & Make Call (Twilio)")
    to_number = st.text_input("Recipient Number (+91...)")
    sms_message = st.text_input("SMS Message")
    if st.button("Send SMS"):
        try:
            client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
            message = client.messages.create(
                body=sms_message,
                from_=os.getenv("TWILIO_PHONE"),
                to=to_number
            )
            st.success("SMS sent successfully!")
        except Exception as e:
            st.error(f"Failed: {e}")

    call_message = st.text_input("Text to Speak (Phone Call)")
    if st.button("Make Call"):
        try:
            client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
            call = client.calls.create(
                twiml=f'<Response><Say>{call_message}</Say></Response>',
                from_=os.getenv("TWILIO_PHONE"),
                to=to_number
            )
            st.success("Call initiated!")
        except Exception as e:
            st.error(f"Failed: {e}")

# -------- LinkedIn --------
with tab3:
    st.header("💼 Post on LinkedIn")
    st.info("Use LinkedIn API with OAuth 2.0 and Marketing Developer permissions.")
    st.text("This is a placeholder due to OAuth complexity.")

# -------- Twitter --------
with tab4:
    st.header("🐦 Post on Twitter")
    tweet = st.text_area("Your Tweet")
    if st.button("Post Tweet"):
        try:
            auth = tweepy.OAuth1UserHandler(
                os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"),
                os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET")
            )
            api = tweepy.API(auth)
            api.update_status(tweet)
            st.success("Tweet posted!")
        except Exception as e:
            st.error(f"Failed: {e}")

# -------- Facebook --------
with tab5:
    st.header("📘 Share on Facebook")
    st.info("You must register an App on Facebook Developer and use Graph API.")
    st.text("This is a placeholder for API setup.")

# -------- Instagram --------
with tab6:
    st.header("📸 Post on Instagram")
    st.info("Using instagrapi (requires login via username/password)")
    username = st.text_input("Instagram Username")
    password = st.text_input("Instagram Password", type="password")
    image_path = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    caption = st.text_area("Caption")
    if st.button("Post on Instagram"):
        try:
            cl = InstaClient()
            cl.login(username, password)
            if image_path is not None:
                with open("temp.jpg", "wb") as f:
                    f.write(image_path.read())
                cl.photo_upload("temp.jpg", caption)
                st.success("Posted to Instagram!")
        except Exception as e:
            st.error(f"Failed: {e}")

# -------- WhatsApp --------
with tab7:
    st.header("🟢 Send Message on WhatsApp (Twilio)")
    wa_number = st.text_input("WhatsApp Number (+91...)")
    wa_msg = st.text_input("Message")
    if st.button("Send WhatsApp"):
        try:
            client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
            message = client.messages.create(
                body=wa_msg,
                from_='whatsapp:' + os.getenv("TWILIO_WHATSAPP"),
                to='whatsapp:' + wa_number
            )
            st.success("Message sent on WhatsApp!")
        except Exception as e:
            st.error(f"Failed: {e}")

# -------- Combine All --------
with tab8:
    st.header("🧩 Send to All Platforms")
    combined_message = st.text_area("Enter Message for All Platforms")
    email_all = st.checkbox("Email")
    sms_all = st.checkbox("SMS")
    twitter_all = st.checkbox("Twitter")
    whatsapp_all = st.checkbox("WhatsApp")
    
    if st.button("Send All"):
        if email_all:
            try:
                yag = yagmail.SMTP(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
                yag.send(to=email_to, subject="Mass Message", contents=combined_message)
                st.success("Email sent!")
            except Exception as e:
                st.error(f"Email Error: {e}")
        if sms_all:
            try:
                client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
                message = client.messages.create(
                    body=combined_message,
                    from_=os.getenv("TWILIO_PHONE"),
                    to=to_number
                )
                st.success("SMS sent!")
            except Exception as e:
                st.error(f"SMS Error: {e}")
        if twitter_all:
            try:
                auth = tweepy.OAuth1UserHandler(
                    os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"),
                    os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET")
                )
                api = tweepy.API(auth)
                api.update_status(combined_message)
                st.success("Tweet posted!")
            except Exception as e:
                st.error(f"Twitter Error: {e}")
        if whatsapp_all:
            try:
                client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
                message = client.messages.create(
                    body=combined_message,
                    from_='whatsapp:' + os.getenv("TWILIO_WHATSAPP"),
                    to='whatsapp:' + wa_number
                )
                st.success("WhatsApp sent!")
            except Exception as e:
                st.error(f"WhatsApp Error: {e}")
