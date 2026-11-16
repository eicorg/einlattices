# Publish the preinjector

Use one working branch, `preinj`. It contains the complete repository, including
other teams' files. Your changes belong in `Preinjector/`, `LTR/`, and `BAR/`.

Run this with Python 3, Git, and GitHub CLI (`gh`) installed. Sign in once with
`gh auth login --hostname github.com`; choose SSH to match the existing Git
connection to `eicorg/einlattices`.

```sh
cd "/Users/wange/Documents/Research/eRHIC injector/eRHIC baseline/Beamline/Lattice/Preinj/control"
python3 publish_preinj.py -m "Update preinjector, LTR, and BAR lattices"
```

The script must be in the `control` repository root, with `preinj` checked out.
It can also be invoked by its full path from another folder.

1. Fetch GitHub's latest branches. Stop if GitHub `preinj` has commits missing
   locally, or if local changes are outside your three folders and the publishing
   files (`publish_preinj.py`, `PUBLISH_PREINJ.md`, and an optional `.gitignore`).
2. Stage your changes and commit with the supplied `-m` message. Excel lock
   files (`~$*`) and `.DS_Store` are excluded. Skip the commit if nothing changed.
3. Merge the latest fetched `main` into `preinj`, preserving your committed
   Preinjector/LTR/BAR edits and bringing in updates to all systems, including
   RCS and RTE. Stop on conflicts so you can resolve them. Before pushing, check
   that the branch has no differences from `main` outside your work scope.
   Push the complete `preinj` branch with a normal push, never a force-push.
4. Open a pull request directly from `preinj` into `main`, or print the link
   to the existing open request, which the push has updated. Skip creating a
   request if the branch contents already match `main`.

BAR and LTR are merged with main rather than replaced, so your own edits in
those folders are retained. RCS, RTE, and other teams' files stay in the branch.
The script keeps `preinj` checked out and creates no extra review branch.
A reviewer performs the actual merge into `main` on GitHub.

If merging reports conflicts, edit the conflicted files to resolve them, stage
the resolved paths with `git add`, and run `git commit` to finish the merge.
Then rerun the publishing command. To cancel an in-progress merge, use
`git merge --abort`; your earlier local work commit remains available.

If the script reports differences outside your work scope, review those paths
and restore them from `origin/main` as appropriate before rerunning. It never
automatically discards those changes.

Use `python3 publish_preinj.py --help` for usage. A failed command stops the
workflow; completed commits and pushes remain. Rerunning skips unchanged commits
and reuses an existing pull request. Existing pull-request titles and descriptions
are preserved; `-m` supplies the title only when a new request is created.
