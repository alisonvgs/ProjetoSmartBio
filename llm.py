import requests

def llm_com_llama3(prompt, model="llama3"):
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        resposta = response.json()
        return resposta.get("response", "")
    except requests.RequestException as e:
        return f"Erro na requisição: {e}"
