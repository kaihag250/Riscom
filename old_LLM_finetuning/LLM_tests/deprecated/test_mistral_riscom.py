import requests

prompt = ": Please extract the following information, if possible and only if it is directly given in the sentence. " \
"Please dont do calculations on your own. The base risk, the new absolute risk, " \
"the relative risk. Name the name of the number and then the number itself. Remember, dont do calculations on your own. " \
"If the wanted number is not directly given, just answer with 'number not directly given'" \
"Here is the sentence from which you have to extract the information: The risk of heart failure is 10%. Alcohol doubles this risk."

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
)

output = response.json()["response"]
print("🔍 Antwort vom Modell:\n", output)

#push Kai