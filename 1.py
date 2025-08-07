import sys
import tempfile
import os
from git import Repo
from config import START_DATE, END_DATE
import datetime

def clone_or_get_repo(repo_url, tmp_dir):
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = os.path.join(tmp_dir, repo_name)
    if os.path.exists(repo_path):
        print(f"Repo already cloned at: {repo_path}")
        repo = Repo(repo_path)
    else:
        print(f"Cloning {repo_url} ...")
        repo = Repo.clone_from(repo_url, repo_path)
    return repo

def analyze_contributions(repo):
    contributor_stats = {}

    for commit in repo.iter_commits('--all', since=START_DATE.isoformat()):
        if not commit.author or not commit.stats:
            continue

        commit_date = datetime.datetime.fromtimestamp(commit.committed_date)
        if commit_date < START_DATE or commit_date > END_DATE:
            continue

        author = commit.author.email or commit.author.name or "Unknown"
        
        if author not in contributor_stats:
            contributor_stats[author] = {"added": 0, "removed": 0}

        stats = commit.stats.total
        contributor_stats[author]["added"] += stats.get("insertions", 0)
        contributor_stats[author]["removed"] += stats.get("deletions", 0)

    return contributor_stats

def output_table(stats):

    print("\n Author wise LOC Contributions Since 01-Jan-2023:\n")

    for author in stats:
        added = stats[author]["added"]
        removed = stats[author]["removed"]
        net = added - removed
        print(f"Author       : {author}")
        print(f"  Lines Added   : {added}")
        print(f"  Lines Removed : {removed}")
        print(f"  Net LOC       : {net}")
        print("-" * 40)


def main():
    if len(sys.argv) != 2:
        print("You need to provide the github repository url as: 1.py <name of the repository whose stats you want>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo = clone_or_get_repo(repo_url, tmp_dir)
        data = analyze_contributions(repo)
        output_table(data)

if __name__ == "__main__":
    main()