from flask import Flask
import github_api as api

app = Flask(__name__)
@app.route("/github/<user_name>", methods= ["GET"])
def get_user_repo(user_name):
    return api.get_repo_commits(user_name)

if __name__ == "__main__":
    app.run(debug=True)