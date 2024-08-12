import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
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
        messagebox.showwarning("Input Error", "can you try again or may be something else.")

def on_clear_button_click():
    prompt_entry.delete("1.0", tk.END)
    response_display.config(state=tk.NORMAL)
    response_display.delete("1.0", tk.END)
    response_display.config(state=tk.DISABLED)

def show_loading():
    loading_label.grid(row=5, column=0, pady=5)
    root.update_idletasks()

def hide_loading():
    loading_label.grid_forget()

root = tk.Tk()
root.title("meal planner app, Happy meals:)")
root.geometry("600x415")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1  )
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=3) 
root.grid_rowconfigure(4, weight=0)

tk.Label(root, text="what are you craving for:").grid(row=0, column=0, pady=5, padx=5, sticky="ew")
prompt_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=3)
prompt_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

send_button = tk.Button(root, text="ask the model", command=on_send_button_click)
send_button.grid(row=2, column=0, pady=10, padx=5, sticky="ew")

clear_button = tk.Button(root, text="clear", command=on_clear_button_click)
clear_button.grid(row=2, column=1, pady=10, padx=5, sticky="ew")

loading_label = ttk.Label(root, text="thinking...", anchor="center")
loading_label.grid_forget()

tk.Label(root, text="Your recipe:").grid(row=3, column=0, pady=5, padx=5, sticky="ew")
response_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, state=tk.DISABLED)
response_display.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

root.mainloop()
