import yaml
import os
import importlib.util

from ImageCreator.core import assets_directory


def to_json(path):
    with open(path, "r") as yml_in:
        json_out = yaml.safe_load(yml_in)
    return json_out


def plugin_handler(value, plugin_directory):
    """
    Takes in plugins in the plugin format and recursively evaluates them\n
    Plugin format: {"plugin": "PLUGINNAME", "kwargs": {"ANY": "THING"}}

    :param value: dict
    :param plugin_directory: str
    :return evaluated plugin: Any
    """
    if not isinstance(value, dict):
        return value
    elif value.get("plugin", None) is not None:
        plugin = value.get("plugin")

        kwargs_ = value.get("kwargs", {})
        for index, item in kwargs_.copy().items():
            if isinstance(item, dict):
                kwargs_[index] = plugin_handler(item, plugin_directory)

        try:
            spec = importlib.util.spec_from_file_location(plugin, os.path.join(plugin_directory, plugin + ".py"))
            plg = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plg)
            run = f"plg.run(**{kwargs_})"
            val = eval(run)
        except Exception as e:
            print(f"Something in the plugin {plugin} went wrong:")
            print(f"\033[91m{e}\033[0m")
            val = None
        return val
    else:
        return value


def dict_iterator(input_dict: dict, plugin_directory: str):
    """
    Iterates through dictionary and uses plugin_handler to evaluate plugins

    :param plugin_directory: str:
    :param input_dict: dict:
    :return output_dict: dict:
    """
    output_dict = input_dict
    for k, v in output_dict.items():
        if isinstance(v, dict):
            if v.get("plugin", None) is not None:
                output_dict[k] = plugin_handler(v, plugin_directory)
            else:
                dict_iterator(v, plugin_directory)

    return output_dict
