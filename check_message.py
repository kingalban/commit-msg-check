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
    parser.add_argument("COMMIT_EDITMSG", help="name of the input to check against")
    parser.add_argument("-p", "--pattern", type=str, help="regex pattern that the commit-msg-file must match")
    parser.add_argument("-n", "--first-n", type=int, default=1, help="how many commits on the branch should match")
    parser.add_argument("-b", "--default-branch", help="the branch HEAD will be compared to to "
                                                       "find the current branch length")
    parser.add_argument("-r", "--repo-path", default=".")
    parser.add_argument("--debug", action="store_true")

    args, _ = parser.parse_known_args(argv)

    if args.debug:
        print("args:", args)
        print("unparsed args:", _)

    repo = Repo(args.repo_path)

    commit_msg = Path(args.COMMIT_EDITMSG).read_text()
    # this is a commit-msg hook, so it happens before the first commit on the branch
    if get_n_commits_in_branch(repo, args.default_branch) < args.first_n and not re.match(args.pattern, commit_msg):
        print(f"commit message = {commit_msg!r} does not match the pattern {args.pattern}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
