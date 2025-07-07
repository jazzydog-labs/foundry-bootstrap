# Design: improved pyenv installation on Linux

## Rationale
The existing `install/install_pyenv_linux.sh` script simply clones the
`pyenv` repository from GitHub. It does not install the build dependencies
needed for Python versions managed by pyenv and fails when run in an
environment without network access. The TODO asks to improve this script so
that pyenv can be installed together with its dependencies and from an
offline archive when available.

## Approach
1. Install the common build dependencies via `apt-get` when available.
   The installation can be skipped by setting `PYENV_SKIP_DEPS=1` which is
   helpful for test environments.
2. Support an optional environment variable `PYENV_ARCHIVE` pointing to a
   tarball containing a pre‑cloned pyenv repository. When provided the
   archive is extracted into `$HOME/.pyenv` instead of performing a `git`
   clone. This allows offline bootstrapping.
3. Keep the rest of the setup (updating `PATH` and shell configuration)
   unchanged.

## Touchpoints
```
install/install_pyenv_linux.sh  # add deps and offline support
README.md                       # document PYENV_ARCHIVE usage
tests/test_pyenv_offline.py     # new test exercising archive path
TODO.md                         # mark task complete
```

## Alternatives considered
- Embedding the pyenv source directly in the repository. Rejected to keep the
  repo lightweight.
- Installing dependencies with another package manager. Out of scope for now.
