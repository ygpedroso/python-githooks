import os
import shutil
import pytest
from python_githooks.helpers import create_config_file

__BASE_DIR__ = os.path.join(os.environ["PWD"], 'tmp')
__GITHOOKS_BASE_DIR__ = os.path.join(__BASE_DIR__, '.git/hooks')
__GITHOOKS_CONFIGFILE_PATH__ = os.path.join(__BASE_DIR__, '.githooks.ini')


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


@pytest.fixture
def workspace_with_config(workspace_with_git):
    create_config_file(__GITHOOKS_CONFIGFILE_PATH__)
    yield __BASE_DIR__
    os.remove(__GITHOOKS_CONFIGFILE_PATH__)
