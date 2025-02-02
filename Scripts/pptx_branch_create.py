import os
import subprocess
from helpers import get_next_sunday_auto

# This script pushes a new branch with a committed PowerPoint file


BRANCH_PREFIX = 'auto-pptx-upload'

if __name__ == "__main__":
    next_sunday = get_next_sunday_auto('%Y-%m-%d')
    pptx_branch_name = f'{BRANCH_PREFIX}-{next_sunday}'

    os.system('git add Scripts/*.pptx')
    # Operate in a temp branch to avoid clashing with other staged changes when run locally
    os.system(f'git checkout -b {pptx_branch_name}')
    os.system(f'git commit -m "Automatic PPTX file for {next_sunday}"')
    # Use the commit hash to guarantee the push will succeed - also remove temp branch for clean up
    os.system(f'git branch -D {pptx_branch_name}')
    latest_commit = subprocess.check_output('git log -1 --format=%H').decode('utf-8').strip()
    os.system(f'git checkout -b {pptx_branch_name}-{latest_commit}')
    os.system(f'git push origin {pptx_branch_name}-{latest_commit}')
