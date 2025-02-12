import requests
import os
import json

from flask import Flask



def get_github(path: str):
    url = "https://api.github.com"
    token = os.getenv("Github_Token")
    response = requests.get(url+ path, headers={'Authorization': "Bearer " + token})
    response.raise_for_status() 
    return response.json()

def read_commits(user_name, repo_name, page_number, items_per_page):
    return get_github(f"/repos/{user_name}/{repo_name}/commits?page={page_number}&per_page={items_per_page}")


def count_commits(user_name, repo_name: str)-> int:
    page_number = 1
    total_commits = 0
    while(True):
        page = read_commits(user_name, repo_name, page_number, 100)
        page_commits = len(page)
        total_commits += page_commits
        if(page_commits<100):
            break 
        page_number += 1
    return total_commits

   
app = Flask(__name__)
@app.route("/github/<user_name>", methods= ["GET"])
def get_user_repo(user_name):
    try:
        user = get_github(f"/users/{user_name}")
        total_repos = user["public_repos"]
        repo_data = get_github(f"/users/{user_name}/repos?page=1&per_page=100")
        repo_dic = {}
        
        for repo in repo_data :
            repo_name = repo["name"]
            commit_count = count_commits(user_name,repo_name)
            repo_dic.update({repo_name:commit_count})
        
        return repo_dic
    except requests.exceptions.HTTPError as err:
        return "Http Error" + str(err)

if __name__ == "__main__":
    app.run(debug=True)