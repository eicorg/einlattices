#!/usr/bin/env python3
"""Sync BAR/LTR, publish preinj, and request a scoped merge into main."""

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
REPO = "eicorg/einlattices"
REVIEW_BRANCH = "preinj-merge"
SCOPED_PATHS = ("Preinjector", "publish_preinj.py", "PUBLISH_PREINJ.md")


def call(*args, env=None, check=True):
    result = subprocess.run(args, cwd=ROOT, env=env, text=True,
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


def check_sync_folders():
    # Accept a clean folder, or one already synchronized to main by a prior run.
    for folder in ("BAR", "LTR"):
        if (ROOT / folder).is_symlink():
            raise RuntimeError(f"{folder} must be a regular folder, not a symbolic link.")
        snapshots = []
        for ref in ("HEAD", "origin/main"):
            snapshot = {}
            for entry in git("ls-tree", "-rz", ref, "--", folder).split("\0"):
                if entry:
                    meta, name = entry.split("\t", 1)
                    mode, _, sha = meta.split()
                    if not temporary_file(name):
                        snapshot[name] = (mode, sha)
            snapshots.append(snapshot)
        working = {}
        for path in (ROOT / folder).rglob("*"):
            if temporary_file(str(path)):
                continue
            if path.is_symlink():
                mode, data = "120000", os.fsencode(os.readlink(path))
            elif path.is_file():
                mode = "100755" if path.stat().st_mode & 0o111 else "100644"
                data = path.read_bytes()
            else:
                continue
            sha = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            working[str(path.relative_to(ROOT))] = (mode, sha)
        if (working not in snapshots or not (matches("HEAD", folder, staged=True)
                                             or matches("origin/main", folder, staged=True))):
            raise RuntimeError(f"{folder} has local edits or untracked files. Save them "
                               "outside that folder before synchronizing from main.")


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
            raise RuntimeError("Finish the current merge, rebase, or cherry-pick first.")
    if git("ls-files", "--unmerged"):
        raise RuntimeError("Resolve the existing Git conflicts first.")
    call("gh", "auth", "status", "--hostname", "github.com")

    print("1/4 Fetching GitHub and updating BAR/LTR from main...", flush=True)
    git("fetch", "--prune", "origin")
    main_sha = git("rev-parse", "refs/remotes/origin/main")
    remote_sha = git("rev-parse", "refs/remotes/origin/preinj")
    if not is_ancestor(remote_sha, "HEAD"):
        raise RuntimeError("GitHub preinj has commits missing locally. Integrate "
                           "those commits before running again; no files were changed.")
    check_sync_folders()
    git("restore", "--source=" + main_sha, "--staged", "--worktree", "--", "BAR", "LTR")

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
    preinj_sha = git("rev-parse", "HEAD")

    print("3/4 Pushing the control repository to preinj...", flush=True)
    git("push", "origin", preinj_sha + ":refs/heads/preinj")

    print("4/4 Preparing the scoped merge request...", flush=True)
    # A separate index builds on all of main, preserving RCS, RTE, and other systems.
    # This never checks out another branch or changes the working folders.
    with tempfile.TemporaryDirectory(prefix="publish-preinj-") as directory:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(directory) / "index"))
        git("read-tree", main_sha, env=env)
        git("restore", "--source=" + preinj_sha, "--staged", "--", *SCOPED_PATHS, env=env)
        tree = git("write-tree", env=env)
        if tree == git("rev-parse", main_sha + "^{tree}"):
            print("The scoped files already match main; no merge request is needed.")
            return
        previous = git("rev-parse", "--verify", "--quiet",
                       "refs/remotes/origin/" + REVIEW_BRANCH, check=False)
        if (previous and tree == git("rev-parse", previous + "^{tree}")
                and is_ancestor(main_sha, previous)):
            review_sha = previous
        else:
            parents = ["-p", main_sha]
            if previous and previous != main_sha:
                parents += ["-p", previous]
            review_sha = git("commit-tree", tree, *parents, "-m", message)
        # Including the previous review commit as a parent keeps this a normal push.
        git("push", "origin", review_sha + ":refs/heads/" + REVIEW_BRANCH)

        existing = call("gh", "pr", "list", "--repo", REPO, "--base", "main",
                        "--head", REVIEW_BRANCH, "--state", "open", "--json", "url",
                        "--jq", ".[0].url // empty").stdout.strip()
        if existing:
            print("Updated merge request: " + existing)
            return
        body = Path(directory) / "pull-request.md"
        body.write_text(message + "\n\nMerge the Preinjector snapshot and its publishing "
                        "script/documentation from preinj. The review branch starts "
                        "from main and preserves all other paths, including RCS and RTE.\n\n"
                        "BAR and LTR were synchronized locally from main before publishing.\n",
                        encoding="utf-8")
        result = call("gh", "pr", "create", "--repo", REPO, "--base", "main",
                      "--head", REVIEW_BRANCH, "--title", message.splitlines()[0][:240],
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
