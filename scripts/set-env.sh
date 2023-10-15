#!/bin/bash
set -e
set -o pipefail

function apt_update_upgrade {
    apt-get update && apt-get upgrade
}

function install_packages {
    apt-get install -y curl git openssh-client libpq-dev
}

function main {
    apt_update_upgrade
}

main
