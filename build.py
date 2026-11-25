"""src/app_template.html に data/core_data.json を埋め込み、index.html を作る。
使い方: python3 build.py
"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent
tpl = (root / 'src' / 'app_template.html').read_text(encoding='utf-8')
data = json.loads((root / 'data' / 'core_data.json').read_text(encoding='utf-8'))
raw = json.dumps(data, ensure_ascii=False, indent=1).replace('</', '<\\/')
assert tpl.count('DEFAULT_DATA') == 1, 'テンプレート内の DEFAULT_DATA が1か所ではありません'
(root / 'index.html').write_text(tpl.replace('DEFAULT_DATA', raw), encoding='utf-8')
print('index.html を作りました')
