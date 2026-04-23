import streamlit as st
from doc_utils import extract_text
from ai_utils import (
    configure_ai,
    generate_summary,
    generate_questions,
    chat_with_notes,
    simplify_text,
    breakdown_topic
)

# Streamlit Page Configuration
st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

def main():
    st.title("📚 AI Study Assistant")
    st.markdown("Upload your study material, and I'll help you summarize, test your knowledge, and simplify complex ideas!")

    # State management for maintaining info across re-renders
    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = None
        
    if "api_configured" not in st.session_state:
        st.session_state.api_configured = True # Default to True since key is hardcoded

    # Sidebar for Setup and Uploads
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.info("Groq API Key is already configured.")
        
        # Optional: still allow user to override if they want
        new_key = st.text_input("Override API Key (Optional):", type="password")
        if new_key:
            try:
                configure_ai(new_key)
                st.session_state.api_configured = True
                st.success("Custom API Key set!")
            except Exception as e:
                st.error(f"Failed to configure custom API: {e}")
            
        st.markdown("---")
        
        st.header("📄 Upload Material")
        uploaded_file = st.file_uploader("Upload study material", type=["pdf", "docx", "pptx", "txt"])
        
        if uploaded_file is not None and st.button("Extract Text"):
            with st.spinner("Parsing text from PDF..."):
                text = extract_text(uploaded_file)
                
                if text and not text.startswith("Error"):
                    st.session_state.pdf_text = text
                    st.success("Text extraction complete!")
                else:
                    st.error(text)

    # Main Dashboard Logic
    if not st.session_state.api_configured:
        st.info("👈 Please configure your Groq API key in the sidebar to get started.")
        return
        
    if not st.session_state.pdf_text:
        st.info("👈 Waiting for you to upload a PDF and click 'Extract Text'.")
        return

    # Elegant Tabs for separating features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Summary", 
        "❓ Q&A Generator", 
        "🧩 Explain Like I'm 10", 
        "📊 Topic Breakdown", 
        "💬 Ask AI"
    ])

    # 1. AI Summarization
    with tab1:
        st.header("Generate Summarities")
        st.write("Get a quick overview or a comprehensive breakdown of your notes.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Get Short Summary ⚡"):
                with st.spinner("Generating short summary..."):
                    summary = generate_summary(st.session_state.pdf_text, summary_type="short")
                    st.info(summary)
                    
        with col2:
            if st.button("Get Detailed Summary 📖"):
                with st.spinner("Generating detailed summary..."):
                    summary = generate_summary(st.session_state.pdf_text, summary_type="detailed")
                    st.info(summary)

    # 2. Q&A Generation
    with tab2:
        st.header("Test Your Knowledge")
        st.write("Automatically generate important subjective questions, viva (oral) questions, and MCQs based on the context.")
        
        if st.button("Generate Q&A Set"):
            with st.spinner("Formulating questions..."):
                qa_content = generate_questions(st.session_state.pdf_text)
                st.success(qa_content)

    # 3. ELI5 Simplification
    with tab3:
        st.header("Explain Like I'm 10")
        st.write("Too complex? Let the AI simplify the text using basic words and analogies.")
        
        if st.button("Simplify Notes 🧸"):
            with st.spinner("Simplifying..."):
                simplified = simplify_text(st.session_state.pdf_text)
                st.success(simplified)

    # 4. Topic Breakdown
    with tab4:
        st.header("Structured Breakdown")
        st.write("Quickly visualize the main topics, key points, and important definitions.")
        
        if st.button("Analyze & Breakdown Syllabus 🔍"):
            with st.spinner("Analyzing content structure..."):
                breakdown = breakdown_topic(st.session_state.pdf_text)
                st.success(breakdown)

    # 5. Semantic Chat
    with tab5:
        st.header("Chat with your Notes")
        st.write("Ask specific, contextual questions. If the answer isn't in your text, the AI will let you know.")
        
        user_query = st.text_input("What do you want to ask about your notes?", placeholder="Explain the concept of...")
        if st.button("Ask Assistant 💡"):
            if user_query:
                with st.spinner("Searching your context notes..."):
                    answer = chat_with_notes(st.session_state.pdf_text, user_query)
                    st.markdown("### Answer")
                    st.info(answer)
            else:
                st.warning("Please enter a question in the input field above.")

if __name__ == "__main__":
    main()
