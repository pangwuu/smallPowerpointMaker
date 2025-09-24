import os
import sys
from datetime import datetime
from helpers import get_next_sunday_auto, is_running_in_ci

# This script pushes a new branch with a committed PowerPoint file

if __name__ == "__main__":
    next_sunday = get_next_sunday_auto('%Y_%m_%d')
    print(next_sunday)
    try:
        if sys.platform.startswith('win'):
            os.system(f'git add Scripts/{next_sunday}.pptx')
        else:
            os.system(f'git add "Complete slides/{next_sunday}.pptx"')
    except Exception as e:
        print(e)
        sys.exit(1)
    # Operate in a temp branch to avoid clashing with other staged changes when run locally
    if is_running_in_ci():
        os.system(f'git config user.email "bot@pangwuu.com"')
        os.system(f'git config user.name "JohnnyBot"')
    os.system(f'git commit -m "Automatic PPTX file for {next_sunday}"')
    # Use the commit hash to guarantee the push will succeed - also remove temp branch for clean up
    timestamp_hash = datetime.now().timestamp()
    os.system(f'git push origin main')