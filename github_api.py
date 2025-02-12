import requests
import os
import json

def get_github(path: str):
    url = "https://api.github.com"
    token = os.getenv("Github_Token")
    response = requests.get(url+ path, headers={'Authorization': "Bearer " + token})
    response.raise_for_status()    
    return response
respons = get_github(f"/users/avestura/repos?page=1&per_page=1")


def get_repos(user_name, page):
    return get_github(f"/users/{user_name}/repos?page={page}&per_page=100")


def count_commits(user_name, repo_name: str)-> str:
    try:
        commit = get_github(f"/repos/{user_name}/{repo_name}/commits?page=1&per_page=1")
        link = commit.links
        url_str = link["last"]["url"]
        total_commits = url_str.split("page=")[1].split("&")[0]
        return total_commits
    except requests.exceptions.HTTPError as err:
        if (err.response.status_code==409 ):
            return 0


def get_repo_commits(user_name):
    try:
        user = get_github(f"/users/{user_name}")
        user_data = user.json()
        total_repo = user_data["public_repos"]
        repo_page = 1
        last_repo_page = (total_repo//100) +1
        while repo_page <= last_repo_page:
            repo = get_repos(user_name, repo_page)
            repo_data = repo.json()
            repo_dic = {}  
            for repo in repo_data :
                repo_name = repo["name"]
                commit_count = count_commits(user_name,repo_name)
                repo_dic.update({repo_name:commit_count})
            repo_page += 1
        return repo_dic
    except requests.exceptions.HTTPError as err:
        return "Http Error" + str(err)