#!/bin/bash
# This script discovers and runs all unit tests in the 'tests' directory.

echo "Running 3D Print Farm Manager tests..."

# Ensure the script is run from the application root directory
# (where 'app.py' and the 'tests' directory are located)
# No explicit check, but assumes standard execution context.

# Discover and run tests
python3 -m unittest discover -s tests -p "test_*.py"

echo "Tests finished."
