#!/usr/bin/env python3
"""Commit local work, merge main into preinj, push, and request a merge."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
REPO = "eicorg/einlattices"
WORK_FOLDERS = ("Preinjector", "LTR", "BAR")
WORK_FILES = ("publish_preinj.py", "PUBLISH_PREINJ.md", ".gitignore")


def call(*args, check=True):
    result = subprocess.run(args, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip()
                           or f"{args[0]} failed (exit {result.returncode}).")
    return result


def git(*args, **kwargs):
    return call("git", *args, **kwargs).stdout.strip()


def is_ancestor(base, head):
    result = call("git", "merge-base", "--is-ancestor", base, head, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip())
    return result.returncode == 0


def matches(ref, folder, staged=False):
    args = ["git", "diff", "--quiet"]
    if staged:
        args.append("--cached")
    result = call(*args, ref, "--", folder, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip())
    return result.returncode == 0


def temporary_file(name):
    return Path(name).name == ".DS_Store" or Path(name).name.startswith("~$")


def in_work_scope(name):
    return name in WORK_FILES or any(name.startswith(folder + "/") for folder in WORK_FOLDERS)


def check_local_scope():
    names = set()
    for args in (("diff", "--no-renames", "--name-only", "-z", "HEAD"),
                 ("diff", "--cached", "--no-renames", "--name-only", "-z"),
                 ("ls-files", "--others", "--exclude-standard", "-z")):
        names.update(git(*args).split("\0"))
    outside = sorted(name for name in names
                     if name and not temporary_file(name) and not in_work_scope(name))
    if outside:
        raise RuntimeError("Local changes outside Preinjector/LTR/BAR and the publishing "
                           "files must be handled separately:\n" + "\n".join(outside))


def publish(message):
    for program in ("git", "gh"):
        if shutil.which(program) is None:
            raise RuntimeError(f"Install {program} before running this script.")
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT:
        raise RuntimeError("Put this script in the control repository root.")
    if git("symbolic-ref", "--short", "HEAD") != "preinj":
        raise RuntimeError("Switch to the preinj branch before running this script.")
    remote = git("config", "--get", "remote.origin.url").rstrip("/")
    if remote not in (f"git@github.com:{REPO}.git", f"https://github.com/{REPO}",
                      f"https://github.com/{REPO}.git", f"ssh://git@github.com/{REPO}.git"):
        raise RuntimeError(f"origin must point to {REPO}.")
    for marker in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
        if (ROOT / git("rev-parse", "--git-path", marker)).exists():
            raise RuntimeError("Finish the current merge, rebase, or cherry-pick first. "
                               "For merge conflicts, resolve the files, stage them, "
                               "and run git commit before rerunning this script.")
    if git("ls-files", "--unmerged"):
        raise RuntimeError("Resolve the existing Git conflicts first.")
    call("gh", "auth", "status", "--hostname", "github.com")

    print("1/4 Fetching GitHub and checking local changes...", flush=True)
    git("fetch", "--prune", "origin")
    main_sha = git("rev-parse", "refs/remotes/origin/main")
    remote_sha = git("rev-parse", "--verify", "--quiet", "refs/remotes/origin/preinj", check=False)
    if remote_sha and not is_ancestor(remote_sha, "HEAD"):
        raise RuntimeError("GitHub preinj has commits missing locally. Integrate "
                           "those commits before running again; no files were changed.")
    check_local_scope()

    print("2/4 Committing local control changes...", flush=True)
    git("add", "--all", "--", ".", ":(exclude,glob)**/~$*", ":(exclude,glob)**/.DS_Store")
    # Also exclude temporary files that had already been staged before this run.
    staged = git("diff", "--cached", "--name-only", "-z").split("\0")
    excluded = [n for n in staged if n and temporary_file(n)]
    if excluded:
        git("restore", "--staged", "--", *excluded)
    if matches("HEAD", ".", staged=True):
        print("No new changes to commit.")
    else:
        print(git("commit", "-m", message))
    print("3/4 Merging main into preinj and pushing...", flush=True)
    merge = call("git", "merge", "--no-edit", main_sha, check=False)
    if merge.returncode:
        raise RuntimeError((merge.stdout + merge.stderr).strip() +
                           "\nThe merge stopped before pushing. Resolve any conflicts, "
                           "stage the resolved files, run git commit, then rerun this script. "
                           "Use git merge --abort to cancel an in-progress merge.")
    print(merge.stdout.strip())
    outside = [name for name in git("diff", "--no-renames", "--name-only", "-z", main_sha, "HEAD").split("\0")
               if name and not in_work_scope(name)]
    if outside:
        raise RuntimeError("The branch would change other teams' files on main. "
                           "Restore those paths from origin/main before publishing:\n" +
                           "\n".join(outside))
    preinj_sha = git("rev-parse", "HEAD")
    git("push", "origin", preinj_sha + ":refs/heads/preinj")

    print("4/4 Opening or updating the preinj-to-main merge request...", flush=True)
    if matches(main_sha, ".", staged=True):
        print("The branch contents already match main; no merge request is needed.")
        return
    existing = call("gh", "pr", "list", "--repo", REPO, "--base", "main",
                    "--head", "preinj", "--state", "open", "--json", "url",
                    "--jq", ".[0].url // empty").stdout.strip()
    if existing:
        print("Updated merge request: " + existing)
        return
    with tempfile.TemporaryDirectory(prefix="publish-preinj-") as directory:
        body = Path(directory) / "pull-request.md"
        body.write_text(message + "\n\nPublish changes in Preinjector, LTR, BAR, and the "
                        "publishing files directly from preinj to main.\n\n"
                        "The branch includes the latest fetched main. Other teams' files, "
                        "including RCS and RTE, match that main snapshot.\n",
                        encoding="utf-8")
        result = call("gh", "pr", "create", "--repo", REPO, "--base", "main",
                      "--head", "preinj", "--title", message.splitlines()[0][:240],
                      "--body-file", str(body))
        print(result.stdout.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-m", "--message", required=True, help="Commit message and new pull-request title")
    args = parser.parse_args()
    if not args.message.strip():
        parser.error("the commit message must not be empty")
    # Git-specific overrides could direct commands at a different repository/index.
    if any(key in os.environ for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")):
        parser.error("unset GIT_DIR, GIT_WORK_TREE, and GIT_INDEX_FILE before running")
    try:
        publish(args.message.strip())
    except (RuntimeError, OSError) as error:
        print("Error: " + str(error), file=sys.stderr)
        print("Stopped. Any completed commits or pushes remain; fix the issue and rerun.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
