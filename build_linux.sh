#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v java >/dev/null || { echo "Install Java 21 JDK"; exit 1; }
java -version
command -v gradle >/dev/null || { echo "Install Gradle 8.8+"; exit 1; }
gradle clean build
echo "Build output: build/libs/"
