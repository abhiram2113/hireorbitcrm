import ollama

response = ollama.chat(
    model='tinyllama',
    messages=[
        {
            'role': 'user',
            'content': 'Give me top Java developer skills'
        }
    ]
)

print(response['message']['content'])