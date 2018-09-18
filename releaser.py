import os
import sys
import subprocess

import github


token = os.getenv("HEY_GITHUB_TOKEN")

g = github.Github(token)

myRepo = g.get_repo("komuw/hey")  # returns a github.Repository.Repository

# 1.
# then we can call
# myRepo.create_git_tag(tag, message, object, type, tagger=github.GithubObject.NotSet)
# where;
# tag: string eg "v0.0.1"
# message: string
# object: string, The SHA of the git object this is tagging.
# type: string,  The type of the object we're tagging. Normally this is a commit but it can also be a tree or a blob.
existing_tags = myRepo.get_tags()
latest_tag = existing_tags[0]
latest_tag_name = latest_tag.name

new_tag = (
    "v" + latest_tag_name.replace("v", "")[:4] + str(int(latest_tag_name.replace("v", "")[-1]) + 1)
)
tag_message = "new hey tag"
tag_object = "444236a5b56a46bdd74521d363e8f8a1b2635751"  # todo: get this via api
git_tag = myRepo.create_git_tag(
    tag=new_tag,
    message=tag_message,
    object=tag_object,
    type="commit",
    tagger=github.GithubObject.NotSet,
)


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
release_name = "release: {0}".format(new_tag)
notes = ["added new feature1", "fixed bug2"]
release_notes = ""
for i in notes:
    release_notes = release_notes + "- " + i + "\n"

release_msg = """
**releaser:** {releaser}
**version:** {version}
**jira:** {jira_link}
**PR:** {pr_link}
**release_type:** {release_type}
**release_notes:**
{release_notes}
""".format(
    releaser="komuw",
    version=new_tag,
    jira_link="https://komuprod.atlassian.net/browse/JKL-207",
    pr_link="https://github.com/komuw/hey/pull/178",
    release_type="config",
    release_notes=release_notes,
)
myRelease = myRepo.create_git_release(
    tag=new_tag,
    name=release_name,
    message=release_msg,
    draft=False,
    prerelease=False,
    target_commitish=github.GithubObject.NotSet,
)


# 3.
# then,
# python setup.py sdist &&
# python setup.py bdist_wheel
# this will create python packages.
sdist_exitcode, sdist_data = subprocess.getstatusoutput("python setup.py sdist")
print("sdist_data output:\n", sdist_data)
if sdist_exitcode != 0:
    sys.exit(sdist_exitcode)

bdist_wheel_exitcode, bdist_wheel_data = subprocess.getstatusoutput("python setup.py bdist_wheel")
print("bdist_wheel_data output:\n", bdist_wheel_data)
if bdist_wheel_exitcode != 0:
    sys.exit(bdist_wheel_exitcode)

# 4.
# then we call;
# myRelease.upload_asset(path, label='', content_type='') # myRelease is a github.GitRelease.GitRelease
# where;
# path: string, The path to The file name of the asset.
# label: string, An alternate short description of the asset. Used in place of the filename.
# content_type: string, eg "application/zip". github accepts this list of media-types: https://www.iana.org/assignments/media-types/media-types.xhtml
# we use the files created in step3 above in our upload_asset() call as the assets
current_dir = os.getcwd()
distribution_dir = os.path.join(os.getcwd(), "dist")
wheel_file = os.path.join(
    distribution_dir, "hey-{version}-py3-none-any.whl".format(version=new_tag.replace("v", ""))
)
myRelease.upload_asset(
    path=wheel_file, label="hey wheel version={version}".format(version=new_tag), content_type=""
)  # myRelease is a github.GitRelease.GitRelease

# 5.
# then you can install as.
# pip install https://github.com/komuw/hey/releases/download/v0.0.1/hey-0.0.1-py3-none-any.whl

