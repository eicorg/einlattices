# Publish the preinjector

Run this from a terminal with Python 3, Git, and GitHub CLI (`gh`) installed.
Sign in to GitHub CLI once with `gh auth login --hostname github.com`.
The configured Git connection must also have permission to push to
`eicorg/einlattices`.

```sh
cd "/Users/wange/Documents/Research/eRHIC injector/eRHIC baseline/Beamline/Lattice/Preinj/control"
python3 publish_preinj.py -m "Update rr18 preinjector lattice"
```

The script must be saved in the `control` repository root, with `preinj`
checked out. It also works when invoked by its full path from another folder.

1. Fetch the latest GitHub branches, then replace the tracked contents of local
   `BAR` and `LTR` with `main`. Files removed from `main` are removed locally too.
   The script stops before replacement if these folders have local edits or
   non-temporary untracked files. A folder already matching `main` is accepted.
2. Stage the entire control repository and commit its changes with the supplied
   message. This includes Preinjector changes, BAR/LTR synchronization, and any
   other local additions, edits, or deletions. Excel lock files (`~$*`) and
   `.DS_Store` are excluded. An unchanged repository skips the commit.
3. Push the complete `preinj` branch to GitHub with a normal push. The script
   stops if GitHub has `preinj` commits missing locally; it never force-pushes.
4. Prepare and push a separate `preinj-merge` review branch based on the latest
   fetched `main`. It copies only `Preinjector/`, `publish_preinj.py`, and
   `PUBLISH_PREINJ.md` from the published snapshot. Every other path remains as
   it is on `main`, including `RCS`, `RTE`, `BAR`, and `LTR`. Open a pull request
   from `preinj-merge` into `main`, or update the branch of an existing open
   request and print its link. If the scoped files already match `main`, no
   pull request is needed.

The script leaves `preinj` checked out. Opening the pull request requests a
merge; a reviewer still performs the merge on GitHub. No reviewer is assigned
automatically. Other paths pushed to `preinj` are outside this pull request.

Use `python3 publish_preinj.py --help` for usage. A failed command stops the
workflow; completed local commits and remote pushes are retained. After fixing
the reported issue, rerun the same command. Existing commits are not duplicated,
and an existing open pull request is reused.
