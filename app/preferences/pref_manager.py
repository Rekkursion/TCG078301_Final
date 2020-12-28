import json


class PrefManager:
    # the dictionary of the preferences
    pref_dict = None

    # the file path of the preferences json file
    json_file_path = './preferences/pref.json'

    # set a single preference
    @staticmethod
    def set_pref(key, value):
        PrefManager.pref_dict[key] = value
        PrefManager.update_json()

    # get a single preference
    @staticmethod
    def get_pref(key):
        return PrefManager.pref_dict.get(key)

    # update the preferences json file
    @staticmethod
    def update_json():
        with open(PrefManager.json_file_path, 'w') as json_file:
            json.dump(PrefManager.pref_dict, json_file)

    # initially load the preferences from the json file
    @staticmethod
    def init_pref():
        with open(PrefManager.json_file_path) as json_file:
            PrefManager.pref_dict = json.load(json_file)
