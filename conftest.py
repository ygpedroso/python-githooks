import os
import shutil
import pytest

__BASE_DIR__ = os.path.join(os.environ["PWD"], 'tmp')
__GITHOOKS_BASE_DIR__ = os.path.join(__BASE_DIR__, '.git/hooks')


@pytest.fixture
def workspace_without_git():
    os.makedirs(__BASE_DIR__)
    yield __BASE_DIR__
    shutil.rmtree(__BASE_DIR__)


@pytest.fixture
def workspace_with_git():
    os.makedirs(__GITHOOKS_BASE_DIR__)
    yield __BASE_DIR__
    shutil.rmtree(__BASE_DIR__)
