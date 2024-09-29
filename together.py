import os
from together import Together

client = Together(api_key=os.environ.get('TOGETHER_TOKEN'))

response = client.chat.completions.create(
    model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
    messages=[],
    max_tokens=512,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>","<|eom_id|>"],
    stream=True
)
print(response.choices[0].message.content)
