import ollama
import sqlite3
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


basePrompt = "You are going to act as an US tax accountant for Delloite and answer the following questions I have about US tax. Don't tell me you are a tax accountant. Give the answer in html format. My question is "
conn = sqlite3.connect('tax_audit.db', check_same_thread=False)

def create_table():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TaxPromptResponse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            chat TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
create_table()

def insert_prompt_response(session_id, chat, prompt, response):
    cursor = conn.cursor()
    if not session_id:
        res = cursor.execute('''SELECT max(session_id) + 1 from TaxPromptResponse''').fetchone()
        sess = 1
        if res[0] is not None:
            sess = res[0] + 1
        cursor.execute('''
            INSERT INTO TaxPromptResponse (session_id, chat, prompt, response)
            VALUES (?, ?, ?, ?)
        ''', (sess, chat, prompt, response))
    else:
        cursor.execute('''
            INSERT INTO TaxPromptResponse (session_id, chat, prompt, response)
            VALUES (?, ?, ?, ?)
        ''', (session_id, chat, prompt, response))
    conn.commit()
    return session_id if session_id else sess

def get_prompt_response_history(session_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT prompt, response, timestamp, chat FROM TaxPromptResponse
        WHERE session_id = ?
        ORDER BY timestamp ASC
    ''', (session_id,))
    rows = cursor.fetchall()
    return rows

def get_all_prompt_responses():
    cursor = conn.cursor()
    cursor.execute('''
        SELECT session_id, chat FROM TaxPromptResponse
        GROUP BY session_id, chat
        ORDER BY session_id ASC
    ''')
    rows = cursor.fetchall()
    return rows

class Prompt(BaseModel):
    prompt: str
    id: None | int

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/chats')
def get_chats():
    return get_all_prompt_responses()

@app.get('/chat/{id}')
def get_chats(id: str):
    return get_prompt_response_history(int(id))

@app.post("/")
def prompt_question(prompt: Prompt):
    previous = []
    chatName = None
    if prompt.id:
        previous = get_prompt_response_history(prompt.id)
    prev_msgs = []
    for prev in previous:
        chatName = prev[3]
        prev_msgs.append({
            "role": "user",
            "content": prev[0], 
        })
        prev_msgs.append({
            "role": "assistant",
            "content": prev[1],
        })

    if not prev_msgs:
        msg = {"role": "user", "content": basePrompt + prompt.prompt}
        prev_msgs.append(msg)
    else:
        prev_msgs[0]["content"] = basePrompt + prev_msgs[0]["content"]

    res = ollama.chat(model = "llama3.2", messages = prev_msgs)
    ans = res["message"]["content"]

    if not chatName:
        chatName = ollama.chat(model = "llama3.2", messages = [{"role": "user", "content": "Give me a sentence identifier for the below message, and dont give me more than 3 words."+ans}])["message"]["content"]

    sess = insert_prompt_response(prompt.id, chatName, prompt.prompt, ans)
    return {"ans": {ans}, "session_id": sess}
