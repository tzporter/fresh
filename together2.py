import os
from together import Together

client = Together(api_key='57adb8778688ebb68600a6a4526850abf7e1deb091478f70a67cad5b1f7905d7')

response = client.chat.completions.create(
    model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
    messages=[{
                "role": "user",
                "content": [
                        {
                                "type": "text",
                                "text": "bruh"
                        }
            ]},
            {
                "role": "user",
                "content": [
                        {
                                "type": "image_url",
                                "image_url": "image.png"
                        }
                ]
        }],
    max_tokens=512,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>","<|eom_id|>"],
    stream=False
)
# for sentence in response:
#     print(sentence.choices)
#     if sentence == "bruh":
#         print("bruh")
#     else:
#         print("no bruh")
print(response.choices[0].message.content)