from groq import Groq
import time
import os

# API Key configuration: prioritized via environment variable for security.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

client = None

def configure_ai(api_key=GROQ_API_KEY):
    """Configures the Groq API client."""
    global client
    if api_key:
        client = Groq(api_key=api_key)

# Auto-configure on load if key exists
configure_ai(GROQ_API_KEY)




def split_text(text, chunk_size=1500):
    """Splits text into manageable chunks."""
    if not text:
        return []
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def safe_generate(prompt):
    """Retry wrapper for Groq API calls."""
    for i in range(3):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Retry {i+1}: {e}")
            time.sleep(2)
    return "Error: Groq API failed after retries. Please check your key or quota."

# ============================
# 🔥 AI FUNCTIONS
# ============================

def generate_summary(text, summary_type="short"):
    chunks = split_text(text)
    if not chunks:
        return "No text provided for summary."
    
    context_chunk = chunks[0] 
    
    if summary_type == "short":
        prompt = f"Give a short, simple summary of the following material:\n\n{context_chunk}"
    else:
        prompt = f"Give a detailed and comprehensive summary of the following material:\n\n{context_chunk}"
        
    return safe_generate(prompt)

def generate_questions(text):
    chunks = split_text(text)
    if not chunks:
        return "No text provided for question generation."
        
    prompt = f"""
    Based on the following material, generate:
    - 5 Important Subjective Questions
    - 5 Viva/Oral Questions
    - 5 Multiple Choice Questions (MCQs) with correct answers indicated
    
    Format the output clearly with headings.
    
    Material:
    {chunks[0]}
    """
    return safe_generate(prompt)

def chat_with_notes(context, query):
    chunks = split_text(context)
    context_text = chunks[0] if chunks else "No context available."
    
    prompt = f"""
    You are an AI Study Assistant. Answer the question specifically using the context provided below.
    If the answer isn't in the context, say you don't know.
    
    Context:
    {context_text}
    
    Question: {query}
    """
    return safe_generate(prompt)

def simplify_text(text):
    chunks = split_text(text)
    if not chunks:
        return "No text provided to simplify."
        
    prompt = f"Explain the following complex material as if I am 10 years old (ELI5). Use simple analogies:\n\n{chunks[0]}"
    return safe_generate(prompt)

def breakdown_topic(text):
    chunks = split_text(text)
    if not chunks:
        return "No text provided for breakdown."
        
    prompt = f"""
    Analyze the following educational material and break it down into:
    - Main Topics
    - Key Bullet Points
    - Important Definitions
    
    Material:
    {chunks[0]}
    """
    return safe_generate(prompt)
