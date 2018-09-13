import os
from github import Github


token = os.getenv("HEY_GITHUB_TOKEN")

g = Github(token)

myRepo = g.get_repo("hey") # returns a github.Repository.Repository

# 1.
# then we can call 
# myRepo.create_git_tag(tag, message, object, type, tagger=github.GithubObject.NotSet)
# where;
# tag: string eg "v0.0.1"
# message: string
# object: string, The SHA of the git object this is tagging.
# type: string,  The type of the object we're tagging. Normally this is a commit but it can also be a tree or a blob.

# 2.
# then we call:
# myRelease = myRepo.create_git_release(tag, name, message, draft=False, prerelease=False, target_commitish=github.GithubObject.NotSet) # returns github.GitRelease.GitRelease
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

# 3.
# then, 
# python setup.py sdist &&
# python setup.py bdist_wheel
# this will create python packages.

# 4.
# then we call;
# myRelease.upload_asset(path, label='', content_type='') # myRelease is a github.GitRelease.GitRelease
# where;
# path: string, The path to The file name of the asset. 
# label: string, An alternate short description of the asset. Used in place of the filename.
# content_type: string, eg "application/zip". github accepts this list of media-types: https://www.iana.org/assignments/media-types/media-types.xhtml
# we use the files created in step3 above in our upload_asset() call as the assets

# 5.
# then you can install as.
# pip install https://github.com/komuw/hey/releases/download/v0.0.1/hey-0.0.1-py3-none-any.whl
