import os
import subprocess
import pytest
from pathlib import Path

def test_dependencies_locked():
    project_root = Path(__file__).resolve().parent.parent.parent
    lock_files = ['requirements.txt', 'Pipfile.lock', 'poetry.lock', 'uv.lock']
    locked = any((project_root / lf).exists() for lf in lock_files)
    assert locked, 'No dependency lock file found'

def test_test_suite_determinism():
    project_root = Path(__file__).resolve().parent.parent.parent
    cmd = ['pytest', 'tests/c3/', '--ignore=tests/c3/test_reproducibility.py', '-q']
    
    result1 = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
    assert result1.returncode == 0
    
    result2 = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
    assert result2.returncode == 0
    
    def extract_summary(stdout):
        for line in stdout.splitlines():
            if 'passed' in line:
                return line.split(' in ')[0]
        return None
        
    summary1 = extract_summary(result1.stdout)
    summary2 = extract_summary(result2.stdout)
    assert summary1 is not None
    assert summary1 == summary2
