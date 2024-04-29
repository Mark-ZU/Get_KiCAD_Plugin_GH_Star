import os
import re
from github import Github

def read_urls(file):
    with open(file, "r") as f:
        return f.readlines()

def read_repos(file):
    with open(file, "r") as f:
        lines = f.readlines()
        repos = {}
        for line in lines:
            line = line.replace("\n","").strip()
            if line == "":
                continue
            repo, url, star = line.split("|")[1:4]
            repos[repo] = star
        return repos

if __name__ == "__main__":
    # create a Github instance
    g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))

    repos = read_urls("urls.txt")

    repos.extend(read_urls("manual_urls.txt"))

    stored_repos = read_repos("repos.txt")

    for repo in repos:
        try:
            repo_root_url = re.match(r"(https:\/\/github.com\/)\w+\/(\w|_|-|\.)*", repo)[0]
            user, repo_name = repo_root_url.split("/")[-2:]
            # print(f"Repo: {repo_root_url}, User: {user}, Repo: {repo_name}")
            store_repo_name = f"{user}/{repo_name}"
            if store_repo_name in stored_repos:
                # print(f"{store_repo_name}: {stored_repos[store_repo_name]}")
                continue
            repo = g.get_repo(store_repo_name)
            print(f"{repo.full_name}: {repo.stargazers_count}")
            stored_repos[store_repo_name] = repo.stargazers_count
        except:
            print(f"Error:{repo}")
            continue

    stored_repos = dict(sorted(stored_repos.items(), key=lambda x: int(x[1]), reverse=True))
    with open("repos.txt", "w") as f:
        for repo, stars in stored_repos.items():
            f.write(f"|{repo}|https://github.com/{repo}|{stars}|\n")
