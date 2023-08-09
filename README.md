
# commit message check
A pre-commit (project) hook to verify commit messages conform to a pattern. 
Specifically it checks that the first `n` commits on a branch fit the pattern (checking evey commit is trivial with pygrep)
This uses the `commit-msg` stage hook, be sure you have installed that hook.

## the length of which branch?
This tool assumes you are following the common convention of creating small feature branches from a default branch. 
The default branch is found by inspecting `origin/HEAD`, you can overwrite this with the arg `-b=<some-weird-branch>`. 

## usage
Here's an example `.pre-commit-config.yaml` which enforces the first 3 commits on a branch have a message starting like `ABCD-001`, `TICK-33310`

`.pre-commit-config.yaml`
~~~ yaml
default_install_hook_types: [pre-commit, commit-msg]
repos:
  - repo: https://github.com/kingalban/commit-msg-check.git
    rev: v0.1.0
    hooks:
      - id: check-commit-message-pattern
        args: [-n=3, "-p=^[A-Z]{4}-[0-9]+"]

~~~
