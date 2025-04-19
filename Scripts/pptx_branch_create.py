import os
import subprocess
from datetime import datetime
from helpers import get_next_sunday_auto, is_running_in_ci

# This script pushes a new branch with a committed PowerPoint file


BRANCH_PREFIX = 'auto-pptx-upload'

if __name__ == "__main__":
    next_sunday = get_next_sunday_auto('%Y-%m-%d')
    pptx_branch_name = f'{BRANCH_PREFIX}-{next_sunday}'

    os.system('git add Scripts/*.pptx')
    os.system('git add "Complete slides/*.pptx"')
    # Operate in a temp branch to avoid clashing with other staged changes when run locally
    os.system(f'git checkout -b {pptx_branch_name}')
    if is_running_in_ci():
        os.system(f'git config user.email "bot@pangwuu.com"')
        os.system(f'git config user.name "JohnnyBot"')
    os.system(f'git commit -m "Automatic PPTX file for {next_sunday}"')
    # Use the commit hash to guarantee the push will succeed - also remove temp branch for clean up
    timestamp_hash = datetime.now().timestamp()
    os.system(f'git checkout -b {pptx_branch_name}-{timestamp_hash}')
    os.system(f'git branch -D {pptx_branch_name}')
    os.system(f'git push origin {pptx_branch_name}-{timestamp_hash}')
