import json


def settings(key, value=None, delete=None):
    'Изменить/получить ключ из настроек'
    if value is not None:
        try:
            with open(
                'data.json',
                'r',
                encoding='utf-8'
            ) as f:
                data = json.load(f)
            with open(
                'data.json',
                'w',
                encoding='utf-8'
            ) as f:
                data[key] = value
                data = dict(sorted(data.items()))
                return json.dump(data, f, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            with open(
                'data.json',
                'w',
                encoding='utf-8'
            ) as f:
                data = {}
                data[key] = value
                return json.dump(data, f, indent=4)
        except json.decoder.JSONDecodeError:
            with open(
                'data.json',
                'w',
                encoding='utf-8'
            ) as f:
                json.dump({}, f, indent=4)
            return None
    elif delete is not None:
        with open(
            'data.json',
            'r',
            encoding='utf-8'
        ) as f:
            data = json.load(f)
        with open(
            'data.json',
            'w',
            encoding='utf-8'
        ) as f:
            if key in data:
                del data[key]
            return json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        try:
            with open(
                'data.json',
                'r',
                encoding='utf-8'
            ) as f:
                data = json.load(f)
                return data.get(key)
        except json.decoder.JSONDecodeError:
            with open(
                'data.json',
                'w',
                encoding='utf-8'
            ) as f:
                json.dump({}, f, indent=4)
            return None
        except FileNotFoundError:
            with open(
                'data.json',
                'w',
                encoding='utf-8'
            ) as f:
                json.dump({}, f, indent=4)
            return None
