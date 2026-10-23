#!/bin/bash
set -euo pipefail

for topic in created completed failed; do
  awslocal sns create-topic --name "lab-task-${topic}" >/dev/null
done
