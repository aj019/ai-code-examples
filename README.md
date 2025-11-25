---
title: ai-chatbot
app_file: chatbot-using-gradio.py
sdk: gradio
sdk_version: 6.0.0
---
# AI Examples

This project demonstrates examples of different use cases of ai models and agents

## How to Run the Chatbot Example

1. **Clone the repository**

   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a virtual environment (optional but recommended)**

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the requirements**

   ```
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**

   - Create a `.env` file in the project directory with the following content:
     ```
     OPENAI_API_KEY=your-openai-api-key-here
     ```

5. **Run the chatbot script**

   ```
   python chatbot-using-gradio.py
   ```

6. **Interact with the chatbot**

   - After running the script, a local Gradio web interface will open in your browser. Start chatting with the AI!
