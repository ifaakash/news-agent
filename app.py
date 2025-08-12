import requests
import feedparser
from datetime import datetime, timezone
import os

# DEEPSEEK Keys and URL
api_key= "sk-"
deepseek_url= "https://api.deepseek.com/chat/completions"

# Parse the feed
DEVOPS_FEEDS = [
    # Terraform
    "https://github.com/hashicorp/terraform/releases.atom",
    "https://www.hashicorp.com/blog/category/terraform/feed",

    # Google
    "https://news.google.com/rss/search?q=devops",

    # AWS
    "https://aws.amazon.com/new/feed/",
    "https://aws.amazon.com/blogs/devops/feed/",

    # Azure
    "https://azure.microsoft.com/en-us/updates/feed/",

    # GCP
    "https://cloud.google.com/feeds/products.xml",  # Google Cloud updates

    # Kubernetes
    "https://github.com/kubernetes/kubernetes/releases.atom",

    # GitHub Actions
    "https://github.blog/changelog/label/actions/feed/",

    # Docker
    "https://www.docker.com/blog/feed/",

    # GitLab
    "https://about.gitlab.com/releases.xml",

    # Jenkins
    "https://www.jenkins.io/changelog-stable/rss.xml",

    # CNCF blog
    "https://www.cncf.io/feed/"
]

# Summarise the link from the RSS feed
def summarise_with_deepseek(title,link):
    prompt= f"""
    Summarise this artile in 3 sentences and state if it is related to devops:
        Title: {title}
        Link : {link}
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
    for rss_url in DEVOPS_FEEDS:
        print(f"\n--- Fetching from: {rss_url} ---")
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            try:
                published = datetime(*entry.published_parsed[:6]).date()
            except AttributeError:
                continue  # skip if no publish date
            if published == today:
                summary = summarise_with_deepseek(entry.title, entry.link)
                print(f"Title: {entry.title}\nLink: {entry.link}\nSummary: {summary}\n")

if __name__== "__main__":
    get_devops_news()
