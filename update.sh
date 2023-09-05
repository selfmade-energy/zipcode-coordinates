#!/usr/bin/env bash

set -eux -o pipefail

./fetch-data.py

if [ -z "$(git diff --exit-code zipcode_coordinates/data)" ]; then
    echo "No changes to the output on this push; exiting."
    exit 0
fi

export VERSION=$(python -c "from zipcode_coordinates import __version__; print(__version__)")

export GIT_AUTHOR_NAME="Github update bot"
export GIT_AUTHOR_EMAIL="git@github.com"
export GIT_COMMITTER_NAME=$GIT_AUTHOR_NAME
export GIT_COMMITTER_EMAIL=$GIT_AUTHOR_EMAIL

git add zipcode_coordinates/data/*.{py,md5} zipcode_coordinates/__init__.py zipcode_coordinates/version.py

git commit -m "Update zip code coordinates to $VERSION"
git tag --annotate --message="Release $VERSION" $VERSION
git push origin HEAD:main $VERSION
