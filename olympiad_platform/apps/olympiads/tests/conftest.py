from django.core.management import call_command

import pytest


@pytest.fixture(scope='function', autouse=True)
def load_data():
    call_command('loaddata', 'combined_data.json')
