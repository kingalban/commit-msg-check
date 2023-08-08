import re
import sys
import argparse
from git import Repo
from pathlib import Path


def get_n_commits_in_branch(repo, default_branch=None) -> int:
    default_branch = default_branch or str(repo.rev_parse("origin/HEAD").name_rev).partition(" ")[2]
    return int(repo.git.rev_list("--count", "HEAD", f"^{default_branch}"))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser("Asserts the first commit to a branch matches a regex")
    parser.add_argument("--commit-msg-filename", help="name of the input to check against")
    parser.add_argument("-p", "--pattern", type=str, help="regex pattern that the commit-msg-file must match")
    parser.add_argument("-n", "--first-n", type=int, default=1, help="how many commits on the branch should match")
    parser.add_argument("-r", "--repo-path", default=".")

    args, _ = parser.parse_known_args(argv)

    repo = Repo(args.repo_path)

    commit_msg = Path(args.commit_msg_filename).read_text()
    # this is a commit-msg hook, so it happens before the first commit on the branch
    if get_n_commits_in_branch(repo) < args.first_n and not re.match(args.pattern, commit_msg):
        print(f"commit message = {commit_msg!r} does not match the pattern {args.pattern}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
