#!/bin/bash
# Prepare Airflow project for Astronomer deployment
# Replaces symlinks with actual files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AIRFLOW_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$AIRFLOW_DIR")"

echo "Preparing Airflow project for deployment..."
echo "Airflow dir: $AIRFLOW_DIR"
echo "Project root: $PROJECT_ROOT"

# Remove symlinks and copy actual directories
cd "$AIRFLOW_DIR/include"

# Handle extraction
if [ -L extraction ]; then
    echo "Replacing extraction symlink with actual files..."
    rm extraction
    cp -r "$PROJECT_ROOT/extraction" extraction
    echo "  Copied extraction/ ($(ls extraction/*.py | wc -l | tr -d ' ') Python files)"
fi

# Handle dbt
if [ -L dbt ]; then
    echo "Replacing dbt symlink with actual files..."
    rm dbt
    cp -r "$PROJECT_ROOT/dbt" dbt
    echo "  Copied dbt/ ($(find dbt -name '*.sql' | wc -l | tr -d ' ') SQL files)"
fi

echo ""
echo "Done! Project is ready for Astronomer deployment."
echo ""
echo "Next steps:"
echo "  1. cd $AIRFLOW_DIR"
echo "  2. astro deploy"
