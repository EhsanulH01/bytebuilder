"""
Simple test script to verify Gemini integration is working
"""
import os

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Test Gemini initialization
    print("Testing Gemini integration...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        print("❌ Error: GOOGLE_API_KEY not set properly in .env file")
        print("Please get an API key from: https://ai.google.dev/gemini-api/docs/api-key")
        exit(1)
    
    # Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.1,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
    
    # Test a simple query
    print("✅ Gemini initialized successfully!")
    print("Testing with a simple query...")
    
    response = llm.invoke("Hello! Can you help me with PC building?")
    print(f"✅ Gemini response received: {response.content[:100]}...")
    
    print("🎉 Gemini integration is working!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure to install: pip install langchain-google-genai")
except Exception as e:
    print(f"❌ Error: {e}")