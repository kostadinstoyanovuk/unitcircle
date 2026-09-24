# Verification records

The files in this directory record the local package installation and three
successful smoke tests on 2026-09-24. See [COMMANDS.md](COMMANDS.md) for the
commands and [tests.log](tests.log) for the test results. These are development
checks, not validation of a scientific release.

Machine-specific paths in `package-install.log`, `tooling-install.log` and
`installed.lock` are normalised for publication. `<workspace>` denotes the
repository directory and `<temporary-directory>` denotes the temporary build
directory. `installed.lock` is a record of the observed environment, not an
installation input; use `requirements-dev.lock` to reproduce the tooling.
Versions, outcomes, wheel digest and other recorded values are unchanged.

`setuptools-84.0.0.json` is a labelled extract of the retrieved PyPI metadata,
not the original response bytes. It preserves the package version, Python
requirement, official source and metadata URLs, artifact names and sizes,
release timestamps, and SHA-256 digests. Its `original_response_sha256` matches
the retrieval record in `source-provenance.json`; that digest describes the
original response, not this extract. Other source snapshots retain their
upstream content and retrieval details.
The source provenance list also references Lean metadata archived in the
companion [schur-cohn repository](https://github.com/kostadinstoyanovuk/schur-cohn/tree/main/evidence).
