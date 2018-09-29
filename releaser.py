import os
import sys
import subprocess

import yaml
import github


# TODO:
# there is a problem because of parallelism in CI.
# since CI can run in parallel, we could have two people creating releases and the one whose commit
# is older than someone else gets a newer version.


class Releaser:
    def __init__(self, github_token, repo_name):
        self.repo_name = repo_name
        g = github.Github(github_token)
        self.myRepo = g.get_repo(self.repo_name)  # returns a github.Repository.Repository

    def calculate_next_tag(self, latest_tag_name):
        """
        given the current tag, calculate the next one.
        eg:
          if latest_tag_name == 'v0.0.10'
          then this method should return 'v0.0.11'
        This method is on it's own so that we can properly test it's implementation.
        Currently we only increment the patch of semver, this method should be extended
        so that it can also be able to increment major/minor versions as required.
        """
        new_tag = (
            "v"
            + latest_tag_name.replace("v", "")[:4]
            + str(int(latest_tag_name.replace("v", "").split(".")[-1]) + 1)
        )
        return new_tag

    def create_tag(self):
        """
        1.
        we can call
        myRepo.create_git_tag(tag, message, object, type, tagger=github.GithubObject.NotSet)
        where;
        tag: string eg "v0.0.1"
        message: string
        object: string, The SHA of the git object this is tagging.
        type: string,  The type of the object we're tagging.
          Normally this is a commit but it can also be a tree or a blob.
        """
        existing_tags = self.myRepo.get_tags()
        print("existing_tags:", existing_tags)
        latest_tag = existing_tags[0]
        print("latest_tag:", latest_tag)
        latest_tag_name = latest_tag.name  # eg; 'v0.0.10'
        new_tag = self.calculate_next_tag(latest_tag_name=latest_tag_name)
        tag_message = "tag:{tag}".format(tag=new_tag)
        tag_object = current_sha
        print(
            "creating git tag. tag={tag}. message={message}. commit={commit}".format(
                tag=new_tag, message=tag_message, commit=tag_object
            )
        )
        git_tag = self.myRepo.create_git_tag(
            tag=new_tag,
            message=tag_message,
            object=tag_object,
            type="commit",
            tagger=github.GithubObject.NotSet,
        )
        print(
            "successfully created git tag. tag={tag}. message={message}. commit={commit}".format(
                tag=new_tag, message=tag_message, commit=tag_object
            )
        )
        return git_tag

    def create_release(self, new_tag, github_user):
        """
        2.
        then we call:
        myRelease = myRepo.create_git_release(tag,
                                             name,
                                             message,
                                             draft=False,
                                             prerelease=False,
                                             target_commitish=github.GithubObject.NotSet)
                                             # returns github.GitRelease.GitRelease
        where;
        tag: string eg "v0.0.1"
        name: string, The name of the release.
        message: string, this is the body, Text describing the contents of the tag.
        target_commitish:  string or
                        :class:`github.Branch.Branch` or
                        :class:`github.Commit.Commit` or
                        :class:`github.GitCommit.GitCommit`
                            Specifies the commitish value that determines
                            where the Git tag is created from.
                            Can be any branch or commit SHA. Unused if the Git tag already exists.
                            Default: the repository's default branch(master)
                            """
        release_name = "release: {0}".format(new_tag)

        f = open(".github/RELEASE_DATA.yaml")
        release_data = yaml.load(f.read())
        f.close()
        rel_notes = release_data["release_notes"]
        release_notes = ""
        for i in rel_notes:
            release_notes = release_notes + "- " + i + "\n"

        # formatted this way so as to conform with markdown
        release_msg = """
**install_instructions:**
you can install this release as:
`pip install git+git://github.com/{repo_name}.git@{version}#egg=hey`
alternatively, you could add the following to your `requirements.txt` file:
`-e git://github.com/{repo_name}.git@{version}#egg=hey`

**releaser:** {releaser}
**version:** {version}
**jira:** {jira_link}
**pull_request:** {pr_link}
**release_type:** {release_type}
**release_notes:**
{release_notes}
        """.format(
            releaser=github_user,
            version=new_tag,
            jira_link=release_data["jira_card"],
            pr_link=release_data["pull_request"],
            release_type=release_data["release_type"],
            release_notes=release_notes,
            repo_name=self.repo_name,
        )
        print(
            "creating git release. tag={tag}. name={name}. message={message}".format(
                tag=new_tag, name=release_name, message=release_msg
            )
        )
        myRelease = self.myRepo.create_git_release(
            tag=new_tag,
            name=release_name,
            message=release_msg,
            draft=False,
            prerelease=False,
            target_commitish=github.GithubObject.NotSet,
        )
        print(
            "successfully created git release. tag={tag}. name={name}. message={message}".format(
                tag=new_tag, name=release_name, message=release_msg
            )
        )
        return myRelease

    def create_distribution(self):
        """
        3.
        then,
        python setup.py sdist &&
        python setup.py bdist_wheel
        this will create python packages.
        """
        print("creating sdist distribution")
        sdist_exitcode, sdist_data = subprocess.getstatusoutput("python setup.py sdist")
        print("sdist_data output:\n", sdist_data)
        if sdist_exitcode != 0:
            sys.exit(sdist_exitcode)

        print("creating bdist_wheel distribution")
        bdist_wheel_exitcode, bdist_wheel_data = subprocess.getstatusoutput(
            "python setup.py bdist_wheel"
        )
        print("bdist_wheel_data output:\n", bdist_wheel_data)
        if bdist_wheel_exitcode != 0:
            sys.exit(bdist_wheel_exitcode)
        print("successfully created  distribution.")

    def upload_assets(self, new_tag, release):
        """
        4.
        then we call;
        myRelease.upload_asset(path, label='', content_type='')
        # myRelease is a github.GitRelease.GitRelease
        where;
        path: string, The path to The file name of the asset.
        label: string, An alternate short description of the asset. Used in place of the filename.
        content_type: string, eg "application/zip".
        github accepts this list of media-types:
          https://www.iana.org/assignments/media-types/media-types.xhtml
        we use the files created in step 3 above in our upload_asset() call as the assets
        """
        distribution_dir = os.path.join(os.getcwd(), "dist")
        wheel_file = os.path.join(distribution_dir, "hey-0.0.1-py3-none-any.whl")
        label = "hey wheel version={version}".format(version=new_tag)
        print(
            "creating release asset. path={path}. label={label}.".format(
                path=wheel_file, label=label
            )
        )
        release.upload_asset(
            path=wheel_file, label=label, content_type=""
        )  # myRelease is a github.GitRelease.GitRelease

    # 5.
    # then you can install as.
    # pip install git+git://github.com/komuw/hey.git@v0.0.24#egg=hey

    # or you can also put the following in your requirements.txt
    # -e git://github.com/komuw/hey.git@v0.0.24#egg=hey


if __name__ == "__main__":
    github_token = os.environ["HEY_GITHUB_TOKEN"]
    pr_link = "cool"  # get this from somewhere, release notes file?
    current_sha = os.environ["CIRCLE_SHA1"]
    user_name = os.environ["CIRCLE_USERNAME"]
    branch_been_built = os.environ["CIRCLE_BRANCH"]

    if branch_been_built != "master":
        print("\n Not master branch. We wont create a new release.")
        sys.exit(0)
    releaser = Releaser(github_token=github_token, repo_name="komuw/hey")
    git_tag = releaser.create_tag()
    release = releaser.create_release(new_tag=git_tag.tag, github_user="@" + user_name)
    releaser.create_distribution()
    releaser.upload_assets(new_tag=git_tag.tag, release=release)
    print(
        "successfully created a new release. release_url={release_url}.".format(
            release_url=release.url
        )
    )
