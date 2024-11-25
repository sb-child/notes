#!/bin/sh

echo "--- origin ---"
git push origin # 本地 gitea
echo "--- github ---"
git push gh # GitHub
echo "--- codeberg ---"
git push codeberg # codeberg