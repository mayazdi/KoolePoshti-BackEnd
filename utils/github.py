from github import Github
from config import config_map

def normalize_languages(dic):
    total = sum(dic.values(), 0.0)
    dic = {k: 100 * v / total for k, v in dic.items()}
    return dic


def get_readme_file(repository):
    try:
        return repository.get_contents("README.md")
    except:
        return None


def deocode_contentfile(readme_contentfile):
    try:
        return readme_contentfile.decoded_content.decode("utf-8")
    except:
        return None


def get_repository_information(repo_address):
    g = Github(config_map['github_accesstoken'])
    repo_info = {}
    try:
        repository = g.get_repo(repo_address)
        repo_info = {
            'readme_content' : deocode_contentfile(get_readme_file(repository)),
            'stars' : repository.stargazers_count,
            'forks' : repository.forks_count,
            'topics' : repository.get_topics(),
            'about' : repository.description,
            'language' : repository.language,
            'languages' : normalize_languages(repository.get_languages()),
            # 'contributors' : repository.get_contributors()
        }
    except:
        repo_info = {"err" : "Repository not found or private"}
    return repo_info
