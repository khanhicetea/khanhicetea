from bs4 import BeautifulSoup
import requests
import datetime

now = datetime.datetime.now()
s = requests.Session()

def fetch(url, data=None):
    if data is None:
        return s.get(url).content
    else:
        return s.post(url, data=data).content

HOMEPAGE = "https://khanhicetea.com"
soup = BeautifulSoup(fetch(HOMEPAGE), "html.parser")

posts = []

for a in soup.select('h2 > a[href*="/posts/"]'):
    posts.append({
        "url": f"{HOMEPAGE}{a.get('href')}",
        "title": a.text,
    })

markdown_links = []

for post in posts:
    markdown_links.append(f"- [{post['title']}]({post['url']})")

with open('README.template.md', 'r') as template_file:
    template_content = template_file.read().rstrip()
    new_content = template_content.replace('@@@LATEST_BLOG_POSTS@@@', "\n".join(markdown_links))
    new_content = new_content.replace('@@@UPDATED_AT@@@', now.strftime("%Y-%m-%d %H:%M:%S"))

    with open('README.md', 'w') as readme_file:
        readme_file.write(new_content)

        print("Done")
        exit(0)

exit(1)
