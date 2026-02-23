import copy

from plf.utils import hash_args, get_invalid_loc_queries, filter_configs


def test_hash_args_is_order_independent_for_dict_keys():
    args_a = {
        "workflow": {"loc": "pkg.workflow.DemoFlow", "args": {}},
        "args": {"model": {"loc": "pkg.model.ModelA", "args": {"lr": 0.1}}},
    }
    args_b = {
        "args": {"model": {"args": {"lr": 0.1}, "loc": "pkg.model.ModelA"}},
        "workflow": {"args": {}, "loc": "pkg.workflow.DemoFlow"},
    }

    assert hash_args(args_a) == hash_args(args_b)


def test_get_invalid_loc_queries_reports_nested_invalid_locs():
    config = {
        "workflow": {"loc": "pkg.workflow.ValidFlow", "args": {}},
        "args": {
            "valid_comp": {"loc": "pkg.component.ValidComp", "args": {}},
            "invalid_comp": {"loc": "InvalidComp", "args": {}},
            "nested": [{"loc": 123, "args": {}}],
        },
    }

    invalid_paths = get_invalid_loc_queries(config)

    assert "args>invalid_comp" in invalid_paths
    assert "args>nested[0]" in invalid_paths
    assert "workflow" not in invalid_paths


def test_filter_configs_supports_key_and_key_value_queries():
    configs = {
        "ppl_a": {
            "model": {"loc": "pkg.model.ResNet", "args": {"depth": 18}},
            "seed": 42,
        },
        "ppl_b": {
            "model": {"loc": "pkg.model.ViT", "args": {"depth": 12}},
            "seed": 7,
        },
    }

    def loader(pplid: str):
        return copy.deepcopy(configs[pplid])

    ids = list(configs.keys())

    assert filter_configs("model", ids, loader) == ids
    assert filter_configs("model=", ids, loader).index.tolist() == ids
    assert filter_configs("seed=42", ids, loader) == ["ppl_a"]
