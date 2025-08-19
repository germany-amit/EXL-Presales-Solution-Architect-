import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import io
from textblob import TextBlob

# -------------------------------
# Title & Intro
# -------------------------------
st.set_page_config(page_title="EXL Pre-Sales & CX Solutioning Studio", layout="wide")

st.title("🤖 EXL Pre-Sales & CX Solutioning Studio")
st.markdown(
    """
    Welcome to the **AI-powered Pre-Sales & CX Solutioning MVP**.  
    This demo showcases skills in **Pre-Sales, Solutioning, CX Journey Mapping, and Contact Center Analytics** –
    exactly aligned with EXL Service's job role requirements.  
    ---
    """
)

# -------------------------------
# Tabs
# -------------------------------
tabs = st.tabs(["📑 Pre-Sales Proposal Generator", "🛠 CX Journey Mapper", "📊 Contact Center Analytics"])

# -------------------------------
# Tab 1: Pre-Sales Proposal Generator
# -------------------------------
with tabs[0]:
    st.header("📑 Pre-Sales Proposal Generator")

    st.markdown("Upload a sample RFP / Requirement text, and generate a structured proposal draft.")

    uploaded_file = st.file_uploader("Upload RFP (TXT)", type=["txt"])
    if uploaded_file is not None:
        rfp_text = uploaded_file.read().decode("utf-8")

        st.subheader("📄 RFP Content")
        st.write(rfp_text)

        # Simple AI-style structured response
        st.subheader("📝 Auto-Generated Proposal Draft")
        proposal = f"""
        ### Executive Summary
        Based on the RFP, the solution will focus on **Omnichannel CX, Conversational AI, and Analytics**.

        ### Proposed Solution
        - Deploy CCaaS platform (Genesys / Amazon Connect / NICE CXone) with integration to CRM.
        - Conversational AI (Voicebot + Chatbot) for customer self-service.
        - Agent Assist tools to improve productivity.
        - Analytics dashboard for speech/text insights and predictive modeling.

        ### Business Value
        - Improve CX by reducing Average Handling Time (AHT).
        - Increase First Call Resolution (FCR) rates.
        - Enhance customer satisfaction (NPS).
        - Scalable & future-ready architecture.
        """
        st.markdown(proposal)

        # Option to download proposal
        buf = io.BytesIO()
        buf.write(proposal.encode())
        st.download_button("⬇️ Download Proposal (TXT)", buf, "proposal.txt")

# -------------------------------
# Tab 2: CX Journey Mapper
# -------------------------------
with tabs[1]:
    st.header("🛠 CX Journey Mapper")

    st.markdown("Enter customer touchpoints to visualize a **Customer Journey Map**.")

    journey_input = st.text_area("Enter journey touchpoints (comma separated):", 
                                 "Website, Chatbot, Agent, Payment, Email Follow-up, Feedback")

    if st.button("Generate Journey Map"):
        steps = [s.strip() for s in journey_input.split(",")]

        # Build graph
        G = nx.DiGraph()
        for i in range(len(steps)-1):
            G.add_edge(steps[i], steps[i+1])

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(6,4))
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, arrows=True)
        st.pyplot(plt.gcf())

# -------------------------------
# Tab 3: Contact Center Analytics
# -------------------------------
with tabs[2]:
    st.header("📊 Contact Center Analytics")

    st.markdown("Upload a CSV with customer transcripts (`text` column required). Example provided below.")

    sample_csv = pd.DataFrame({
        "text": [
            "I am very unhappy with your service.",
            "The agent was helpful and solved my problem quickly.",
            "Waiting time was too long, very frustrating.",
            "Great support, I am satisfied with the resolution."
        ]
    })

    st.download_button(
        "⬇️ Download Sample Transcript CSV",
        sample_csv.to_csv(index=False).encode(),
        "sample_transcripts.csv"
    )

    uploaded_csv = st.file_uploader("Upload Transcript CSV", type=["csv"])
    if uploaded_csv is not None:
        df = pd.read_csv(uploaded_csv)

        st.subheader("📂 Uploaded Data")
        st.write(df.head())

        st.subheader("📊 Sentiment Analysis")
        sentiments = df["text"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        df["sentiment"] = sentiments

        st.write(df)

        # Plot sentiment
        plt.figure(figsize=(6,4))
        plt.hist(sentiments, bins=5, color="skyblue", edgecolor="black")
        plt.xlabel("Sentiment Score (-1 negative to +1 positive)")
        plt.ylabel("Count")
        plt.title("Sentiment Distribution")
        st.pyplot(plt.gcf())
