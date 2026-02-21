import copy

import pytest

from plf._pipeline import PipeLine
from plf.experiment import get_ppls


class _FakeWorkflow:
    def __init__(self):
        self.template = {"model"}
        self.paths = ["artifact"]
        self.ran = False

    def new(self, args):
        if "model" not in args:
            raise ValueError("model config is required")

    def prepare(self):
        return True

    def run(self):
        self.ran = True

    def get_path(self, of: str, pplid: str, args=None):
        if of == "artifact":
            return f"Artifacts/{pplid}.txt"
        raise ValueError(f"Unsupported artifact: {of}")

    def clean(self):
        return None

    def status(self):
        return {"state": "ok"}


@pytest.mark.integration
def test_pipeline_new_prepare_run_and_reload(setup_lab_env, monkeypatch):
    def fake_load_component(self, loc: str, args=None, setup=True):
        workflow = _FakeWorkflow()
        workflow.P = self
        return workflow

    monkeypatch.setattr(PipeLine, "load_component", fake_load_component)

    config = {
        "workflow": {"loc": "tests.fake_workflow.MockWorkflow", "args": {}},
        "args": {
            "model": {"loc": "tests.fake_components.MockModel", "args": {"depth": 2}}
        },
    }

    pipeline = PipeLine()
    pipeline.new(pplid="it_pipeline_001", args=copy.deepcopy(config))

    assert pipeline.verify(pplid="it_pipeline_001") == "it_pipeline_001"
    assert "it_pipeline_001" in get_ppls()

    pipeline.prepare()
    assert pipeline._prepared is True

    pipeline.run()
    assert pipeline.is_running() is False

    reloaded = PipeLine(pplid="it_pipeline_001")
    assert reloaded.cnfg["pplid"] == "it_pipeline_001"
