from llm.plugins import pm

def test_plugin_is_installed():
    try:
        from llm.plugins import load_plugins
        load_plugins()
    except ImportError:
        pass
        
    names = [mod.__name__ for mod in pm.get_plugins()]
    assert "llm_deepseek" in names
