import requests
import feedparser
from datetime import datetime, timezone
import os

# DEEPSEEK Keys and URL
api_key= "sk-"
deepseek_url= "https://api.deepseek.com/chat/completions"

# Parse the feed
DEVOPS_FEEDS = [
    "Terraform", "Azure", "AWS", "DevOps", "Devops Automation", "Prometheus", "APM", "AI in DevOps"
]

# Summarise the link from the RSS feed
def summarise_with_deepseek(topic, date):
    prompt= f"""
    Give me three article related to {topic} and give me a detailed summary of it. The article should be with reference to latest date which is {date}.
    You can include open source projects as well that i can try upon, which sounds exciting.
    """

    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    response= requests.post(deepseek_url,json=data,headers=headers)

    # Debug: Print response status and content
    print(f"API Response Status: {response.status_code}")
    print(f"API Response Content: {response.text}")

    if response.status_code != 200:
        return f"API Error: {response.status_code} - {response.text}"

    try:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as e:
        return f"Error parsing response: {e} - Response: {response.text}"

def get_devops_news():
    today = datetime.now(timezone.utc).date()
    for topic in DEVOPS_FEEDS:
        print(f"\n--- Fetching article for : {topic} ---")
        summary = summarise_with_deepseek(topic, today)
        print(f"Summary: {summary}\n")

if __name__== "__main__":
    get_devops_news()
