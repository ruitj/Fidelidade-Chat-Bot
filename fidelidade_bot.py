# fidelidade_bot.py

import re
import time
from langdetect import detect
from openai import AzureOpenAI

API_KEY = "8J6pTdfaGgA5r193UVLsBshUspqwNpal42Jse1aHaok1cWNTLpRkJQQJ99BDACYeBjFXJ3w3AAABACOGLa23"

client = AzureOpenAI(
    azure_endpoint="https://ai-bcds.openai.azure.com/",
    api_key=API_KEY,
    api_version="2024-05-01-preview"
)

assistant = client.beta.assistants.create(
    model="gpt-4o-mini",
    name="Assistant Group N (R)",
    instructions=(
        "Nunca uses mais do que 700 caracteres. Tu és um perito que trabalha na Fidelidade em investimentos a prazo. "
        "Lembra-te que estás a falar com pessoas que não têm formação financeira. Simplifica a linguagem e, por vezes, "
        "faz um pouco de literacia financeira. Recomenda sempre produtos da Fidelidade sempre que for um investimento que "
        "faça sentido. Outros não serão permitidos. Informações não disponíveis nos ficheiros estão fora do teu âmbito, "
        "como tal, diz que não sabes responder a essa questão. Recorre sempre a fontes disponíveis nos ficheiros e faz citações."
    ),
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search": {
            "vector_store_ids": ["vs_2oe1I9LEsJcvJEKmbJnBuLwk"]
        },
        "code_interpreter": {
            "file_ids": [
                "assistant-WuJZaGApRBgPZGvfPJwTBF", "assistant-WQbe2oYNiunshZFamDkAMe",
                "assistant-WA9mo2ooGuCakdtLYe7S5Y", "assistant-VmGKDJtKWW8mLr7RsNDHJ4",
                "assistant-VcoN7vmxYPZCBfSTaFsEQ3", "assistant-TaHujXgSvATXXH1V5gBTDN",
                "assistant-NMXvUzELtRbwtQMoTXeApo", "assistant-LvBZjKCKvtwUvCCTgpfWim",
                "assistant-GWrPgzCPp8si1AH2yKKJBB", "assistant-F5nrFbNEjGxEqeSCmkdLAg",
                "assistant-EwB2EpAtrmQVUrtxvg79HB", "assistant-BFYazbjKgte4W5u9Jgrs6b",
                "assistant-96mBrzvMJbaTjLYcCEG3S2", "assistant-8phYrqvFLjksiThSKqSgkq",
                "assistant-7GHqFyWe29skpMH8Ug4QoZ", "assistant-6zJbn35vHos3RRzqJUiVMQ",
                "assistant-5dMu4U3q2VUkjhP4LvhAGb", "assistant-4hduKqwh6y7AWcUohbxMC3",
                "assistant-426n1B453C2wqH2AnDc2mh", "assistant-3UFjejDd1iMmYhBuj2bgi8"
            ]
        }
    },
    temperature=0.05,
    top_p=0.9
)

thread = client.beta.threads.create()

def detect_language(text):
    try:
        lang = detect(text)
        return 'pt' if lang == 'pt' else 'en'
    except:
        return 'pt'

def chat_with_assistant(user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    lang = detect_language(user_message)
    instructions = "From now on, please respond in Portuguese." if lang == "pt" else "From now on, please respond in English."

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        additional_instructions=instructions
    )

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]

    msg = re.sub(r'【\d+:\d+†source】', '', assistant_messages[0].content[0].text.value)
    return msg
