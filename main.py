import requests
import json


def get_github(path: str):
    url = "https://api.github.com"
    token = "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"
    response = requests.get(url+ path, headers={'Authorization': "Bearer " + token})
    response.raise_for_status()   
    return response

def read_commits(user_name, repo_name, page_number, items_per_page):
    return get_github(f"/repos/{user_name}/{repo_name}/commits?page={page_number}&per_page={items_per_page}")

# def read_repos(user_name, page_number, items_per_page):
#     return get_github(f"/users/{user_name}/repos?page={page_number}&per_page={items_per_page}")

def count_commits(user_name, repo_name: str)-> int:
    page_number = 1
    total_commits = 0
    while(True):
        page = read_commits(user_name, repo_name, page_number, 100)
        page_obj = page.json()
        page_commits = len(page_obj)
        total_commits += page_commits
        if(page_commits<100):
            break 
        page_number += 1
    return total_commits

   

try:
    user_name = input("PLease enter a Username in github.com. \n"
              "I retrieve all of his public repositories with his total commits:")  
    repos_path =  "repos"
    user = get_github(f"/users/{user_name}")
    user_obj = user.json()
    total_repos = user_obj["public_repos"]
    repo = get_github(f"/users/{user_name}/repos?page=1&per_page=100")
    repo_obj = repo.json()
    
    for i in range (total_repos) :
        repo_name = repo_obj[i]["name"]
        commit_counter = count_commits(user_name,repo_name)
        print(f" {repo_name} : {str(commit_counter)}")
except requests.exceptions.HTTPError as err:
    print("Http Error", err)