import os
from github import Github


token = os.getenv("HEY_GITHUB_TOKEN")

g = Github(token)

myRepo = g.get_repo("hey") # returns a github.Repository.Repository

# then we can call 
# myRepo.create_git_tag(tag, message, object, type, tagger=github.GithubObject.NotSet)
# where;
# tag: string eg "v0.0.1"
# message: string
# object: string, The SHA of the git object this is tagging.
# type: string,  The type of the object we're tagging. Normally this is a commit but it can also be a tree or a blob.

# then we call:
# myRepo.create_git_release(tag, name, message, draft=False, prerelease=False, target_commitish=github.GithubObject.NotSet)
# where;
# tag: string eg "v0.0.1"
# name: string, The name of the release.
# message: string, this is the body, Text describing the contents of the tag.
# target_commitish:  string or 
#                    :class:`github.Branch.Branch` or 
#                    :class:`github.Commit.Commit` or 
#                    :class:`github.GitCommit.GitCommit` 
#                     Specifies the commitish value that determines where the Git tag is created from. 
#                     Can be any branch or commit SHA. Unused if the Git tag already exists. 
#                     Default: the repository's default branch(master)
