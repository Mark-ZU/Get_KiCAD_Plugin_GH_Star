import requests
import re
_URL = "https://github.com/devbisme/kicad-3rd-party-tools"

def get_all_github_urls(__URL):
    response = requests.get(__URL)
    if response.status_code == 200:
        urls = []
        for line in response.text.split("\n"):
            if "href=" in line and "github.com" in line:
                url = line.split("href=")[1].split('"')[1]
                # if "github.com" in url and "http" in url:
                # regex to match https://github.com/*/*
                # if re.fullmatch(r"(https:\/\/github.com\/)\w+\/([a-z]|[A-Z]|[0-9]|_|-)*", url):
                if re.fullmatch(r"(https:\/\/github.com\/)\w+\/.*", url):
                    repo_root_url = re.match(r"(https:\/\/github.com\/)\w+\/(\w|_|-|\.)*", url)[0]
                    user, repo_name = repo_root_url.split("/")[-2:]
                    if user not in ["features", "enterprise", "solutions"]:
                        urls.append(url)
        return urls
    else:
        return []

if __name__ == "__main__":
    urls = get_all_github_urls(_URL)
    for url in urls:
        with open("urls.txt", "w") as f:
            f.write(f"{url}\n")