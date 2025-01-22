def test_plugin_is_installed():
    from llm.plugins import pm, load_plugins
    load_plugins()
    names = [mod.__name__ for mod in pm.get_plugins()]
    assert "llm_deepseek" in names
