#!/bin/sh
# entrypoint.sh

# Check if TOKEN is set
if [ -z "$TOKEN" ]; then
  echo "Error: TOKEN environment variable is not set."
  exit 1
fi

# Execute the command
exec "$@"
