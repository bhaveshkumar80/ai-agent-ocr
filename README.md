# 🤖 AI Chatbot with Tools (Streamlit + LangChain + Ollama)

This project is an **AI-powered chatbot** built with **LangChain**, **Ollama**, and **Streamlit**, capable of interacting with multiple tools such as **Weather Data Retrieval**, **OCR (File Text Extraction)**, and **Medical Document Retrieval**.  
It also supports **file uploads** directly in the chat and stores chat history in an SQLite database for future reference.

---

## 🚀 Features

- **Interactive Chat UI** using Streamlit's `st.chat_input` and `st.chat_message`.
- **Multi-Tool Integration** via LangChain Agent:
  1. **Weather Tool** – Retrieves weather data (temperature, humidity, wind, etc.).
  2. **OCR Tool** – Extracts text from images, PDFs, or DOCX files.
  3. **Medical Document Retrieval** – Searches medical knowledge base.
  4. **NoToolNeeded** – Uses AI's own reasoning for general queries.
- **Chat History Awareness** – If a question relates to previous conversation, it answers without calling tools.
- **File Upload Support** – Upload `.jpg`, `.jpeg`, `.png`, `.pdf`, `.docx` directly in chat.
- **Persistent Chat Storage** – Stores all user/AI messages in an SQLite database.
- **Dynamic Session IDs** – Tracks sessions uniquely.

---

## 🛠️ Technologies Used

- **[Python 3.10+](https://www.python.org/)**
- **[Streamlit](https://streamlit.io/)** – Frontend UI for chat.
- **[LangChain](https://www.langchain.com/)** – Orchestration framework for LLM + tools.
- **[Ollama](https://ollama.com/)** – Local LLM hosting (using `llama3.1:8b` model).
- **[dotenv](https://pypi.org/project/python-dotenv/)** – Environment variable management.
- **SQLite** – Local database for storing chats.
- **Tempfile / UUID** – For secure file handling and session tracking.

---

## 📦 Project Structure

.
├── main.py # Main Streamlit chatbot script
├── tools.py # Tool definitions (OCR, RAG, Weather, NoTool)
├── store_chats.py # Functions for initializing DB and storing messages
├── requirements.txt # Python dependencies
├── .env # Environment variables (Ollama, DB path, etc.)
├── README.md # Project documentation
├── data/ #RAG PDF
└── output_file/ # Extracted files through OCR


## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/ai-chatbot-tools.git
cd ai-chatbot-tools

2️⃣ Create a virtual environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies

pip install -r requirements.txt


4️⃣ Install & run Ollama
Download Ollama for your system.
Pull the llama3.1:8b model:

ollama pull llama3.1:8b


5️⃣ Configure .env file
Create a .env file in the project root.
Go to https://www.weatherapi.com/ and signup to create a api key. 

WEATHER_API_KEY="YOUR_API_KEY"


7️⃣ Run the chatbot
streamlit run app.py