import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

def get_llm_response(prompt):
    try:
        chat_session = model.start_chat(
            history=[ 
                {
                    "role": "user",
                    "parts": ["Accurately provide an appropriate recipe consistent with your analysis."]
                }
            ]
        )
        response = chat_session.send_message(prompt, stream=True)
        response_display.config(state=tk.NORMAL)
        response_display.delete("1.0", tk.END)
        for chunk in response:
            response_display.insert(tk.END, chunk.text)
            response_display.see(tk.END)
            response_display.update()
        response_display.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def on_send_button_click():
    prompt = prompt_entry.get("1.0", tk.END).strip()
    if prompt:
        get_llm_response(prompt)
    else:
        messagebox.showwarning("Input Error", "Please enter a prompt.")

root = tk.Tk()
root.title("meal planner app, Happy meals:)")
root.geometry("600x400")
tk.Label(root, text="what are you craving for:").pack(pady=5)
prompt_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=5, width=60)
prompt_entry.pack(pady=5)
send_button = tk.Button(root, text="ask the model", command=on_send_button_click)
send_button.pack(pady=10)
tk.Label(root, text="Your recipe:").pack(pady=5)
response_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=60, state=tk.DISABLED)
response_display.pack(pady=5)
root.mainloop()
