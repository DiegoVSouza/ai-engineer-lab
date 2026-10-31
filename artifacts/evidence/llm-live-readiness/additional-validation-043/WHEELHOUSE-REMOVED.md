# Wheelhouse removed from HEAD

The 37 third-party wheels (about 52 MB) that were here were removed from the current tree on 2026-10-31 so the repository is a reasonable size to clone. They are still in Git history; history was not rewritten.

`wheelhouse-manifest.json` keeps the file name, byte size and SHA-256 of every wheel, and `wheelhouse-coverage.json` and `wheel-download.json` keep the download record. To rebuild the directory, download each file for `cp313-manylinux2014_x86_64` and compare its hash with the manifest. The wheels carry their own third-party licenses.
