from pathlib import Path

import pytest

from plf.lab import get_logs, lab_setup



@pytest.mark.integration
def test_create_project_sets_up_expected_layout(setup_lab_env):
    settings = setup_lab_env["settings"]
    data_path = Path(settings["data_path"])

    assert data_path.exists()
    assert (data_path / "logs.db").exists()
    assert (data_path / "ppls.db").exists()
    assert (data_path / "Archived" / "ppls.db").exists()
    assert (data_path / "Clones").exists()



@pytest.mark.integration
def test_lab_setup_appends_a_new_log_record(setup_lab_env):
    settings = setup_lab_env["settings"]
    before_count = len(get_logs())

    lab_setup(settings["setting_path"])

    after_count = len(get_logs())
    assert after_count == before_count + 1
