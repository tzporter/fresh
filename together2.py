import os
from together import Together
import base64


def generate_json(base64_image):
    # image_path = "image.png"

    client = Together(api_key= os.getenv("TOGETHER_API_KEY"))

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
        messages=[
            {
                "role": "system",
               "content": """You are a fruit and vegetable expert. You will answer the following questions and store them in JSON format. Use the following template and only respond with JSON. Format your JSON with newlines for each new key value pair, ensuring a pair REMAINS ON THE SAME LINE. There should be a comma after each entry except for the final entry. Strings should be in quotes.
{
    "item": //What type of item the fruit or vegetable is. Output in quotation marks,
    "emoji": //An accurate emoji for the input image. If there isn't one, leave as null. Output in quotation marks,
    "quantity": //how many bananas are pictured in the image. If the item is not easily disivible, such as lettuce or grapes, leave as null,
    "ripeness": //Level of ripeness from 1 to 10,
    "time-left": //Time left before expiration in days
}
If the item is of multiple objects, return the following and only the following message:
MultipleObjectsError
If the item is not a fruit or vegetable, return the following and only the following message:
NotFruitOrVegetableError
Think carefully about the number of unique items and the types of items present in order to ensure correct error output.
Examples:
User: Image of cornucopia
Assistant: NotFruitOrVegetableError

User: Image of apples and oranges
Assistant: MultipleObjectsError

User: Image of 10 bananas
Assistant: 
{
"item": "banana",
"emoji": "🍌",
"quantity": 10,
"ripeness": 8,
"time-left": 5
}
Do NOT provide explanation. Be sure to provide emojis when available."""
            },
            {
                "role": "user",
                "content": "submission"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],

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
    return response.choices[0].message.content
    # print(response.choices[0].message.content)