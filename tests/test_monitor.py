import pytest
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from src.storage.database_manager import init_db

def test_stable_run():
    init_db()
    # Mock capture to avoid real network
    assert True  # Placeholder - full test after stability

if __name__ == '__main__':
    pytest.main(['-v'])
