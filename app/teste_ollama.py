import ollama

response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": "Responda apenas: funcionando"
        }
    ]
)

print(response["message"]["content"])