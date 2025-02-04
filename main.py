import requests
import json
import jmespath

def get_github(path: str):
    url = "https://api.github.com"
    token = "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"
    return requests.get(url+ path, headers={'Authorization': "Bearer " + token})
# def commits_counter(commit_obj: object)-> int:



user_name = "/prodehghan"
repos_path =  "/repos"
commits_path = "/commits?per_page=100"
user = get_github(f"/users{user_name}")
print(user.status_code)
repos = get_github(f"/users{user_name}{repos_path}")
print(repos.status_code)
user_obj = user.json()
repos_obj = repos.json()


for i in range (0,user_obj["public_repos"]) :
    repos_name = repos_obj[i]["name"]
    commits = get_github(f"{repos_path}{user_name}/{repos_name}{commits_path}")
    commits_obj = commits.json()
    print(repos_name +":"+str(len(commits_obj)))
    print("\n")


# "commits_url": "https://api.github.com/repos/prodehghan/PerformanceMonitor.WinForms/commits{/sha}",