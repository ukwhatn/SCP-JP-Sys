#!/bin/bash
set -euxo pipefail
cd "$(dirname "$0")"

# reset postgres dir
rm -r ./postgres
