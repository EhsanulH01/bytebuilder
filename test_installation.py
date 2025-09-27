import sys
import os

def test_imports():
    print("🔍 Testing Python packages...")
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"), 
        ("google.generativeai", "Google Generative AI"),
        ("dotenv", "Python-dotenv"),
        ("mcp", "MCP"),
        ("langchain_google_genai", "LangChain Google GenAI"),
        ("requests", "Requests"),
        ("asyncio", "AsyncIO (built-in)")
    ]
    
    missing_packages = []
    for package, name in packages:
        try:
            __import__(package)
            print(f"✅ {name} installed")
        except ImportError:
            print(f"❌ {name} not installed")
            if package not in ["asyncio"]:  # asyncio is built-in
                missing_packages.append(package)
    
    return missing_packages

def test_env():
    print("\n🔍 Testing environment...")
    try:
        from dotenv import load_dotenv
        load_dotenv("ByteBuilderAi/mcp-intro/.env")
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and api_key.strip().startswith("AIza"):
            print("✅ Google API key found and looks valid")
            return True
        else:
            print("❌ Google API key not found or invalid")
            return False
    except Exception as e:
        print(f"❌ Error loading environment: {e}")
        return False

def test_backend_files():
    print("\n🔍 Checking backend files...")
    files_to_check = [
        "ByteBuilderAi/Backend/main.py",
        "requirements.txt",
        "ByteBuilderAi/mcp-intro/.env"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} found")
        else:
            print(f"❌ {file_path} not found")
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("🚀 ByteBuilder API Installation Check\n")
    
    missing = test_imports()
    env_ok = test_env()
    files_ok = test_backend_files()
    
    print("\n" + "="*50)
    if missing:
        print(f"📦 Missing packages: {', '.join(missing)}")
        print("\n🔧 Run this to install missing packages:")
        print(f"pip3 install {' '.join(missing)}")
    else:
        print("✅ All packages installed!")
    
    if not env_ok:
        print("\n⚠️  Check your .env file configuration")
    
    if not files_ok:
        print("\n⚠️  Some required files are missing")
    
    if not missing and env_ok and files_ok:
        print("\n🎉 Everything looks good! You can start the API server.")
        print("\n🚀 To start the server, run:")
        print("python3 ByteBuilderAi/Backend/main.py")
