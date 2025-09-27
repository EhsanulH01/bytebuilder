# Installation Guide - PC Part Picker Project

## Quick Start (Recommended)

To install all dependencies for the entire project:

```bash
pip install -r requirements.txt
```

## Component-Specific Installation

### Backend Only (FastAPI Server)
```bash
cd Backend
pip install -r requirements.txt
```

### MCP Client Only (AI Integration)
```bash
cd ByteBuilderAi/mcp-intro
pip install -r requirements.txt
```

## Setup Instructions

1. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   - Copy `.env.example` to `.env` in `ByteBuilderAi/mcp-intro/`
   - Add your Gemini API key:
     ```
     GOOGLE_API_KEY=your_gemini_api_key_here
     ```
   - Get your API key from: https://ai.google.dev/gemini-api/docs/api-key

3. **Run the Backend Server:**
   ```bash
   python ByteBuilderAi/Backend/main.py
   ```
   - Server will be available at: http://localhost:8000
   - API docs at: http://localhost:8000/docs

4. **Run the Frontend (requires Node.js 20.19+):**
   ```bash
   cd Frontend
   npm run dev
   ```

5. **Run the MCP Client (AI Chat):**
   ```bash
   cd ByteBuilderAi/mcp-intro
   python scout/client.py
   ```

## Testing

Test the backend:
```bash
python test_backend.py
```

Test Gemini integration:
```bash
cd ByteBuilderAi/mcp-intro
python test_gemini.py
```

## Package Explanations

- **fastapi & uvicorn**: Web API framework and server
- **aiohttp & requests**: HTTP clients for web requests
- **beautifulsoup4**: HTML parsing for web scraping
- **langchain-google-genai**: Gemini AI integration
- **pydantic**: Data validation and settings
- **python-dotenv**: Environment variable management
- **mcp packages**: Model Context Protocol for AI tools

## Troubleshooting

If you encounter installation errors:

1. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install specific packages individually:**
   ```bash
   pip install fastapi uvicorn
   pip install langchain-google-genai
   ```

3. **Use virtual environment (recommended):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```