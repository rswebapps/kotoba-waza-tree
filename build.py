"""index.html を、data/core_data.json から作る。
使い方: python3 build.py
- index.html：src/app_template.html に core_data.json と宇宙の画面（src/uchu_template.html）を埋め込む。宇宙はボタンから、いまのデータで別窓に開く
"""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent
data = json.loads((root / 'data' / 'core_data.json').read_text(encoding='utf-8'))
dump = lambda o: json.dumps(o, ensure_ascii=False, indent=1).replace('</', '<\\/')

# ツリー
tpl = (root / 'src' / 'app_template.html').read_text(encoding='utf-8')
ut0 = (root / 'src' / 'uchu_template.html').read_text(encoding='utf-8')
assert tpl.count('UCHU_TEMPLATE') == 1, 'app_template.html の UCHU_TEMPLATE が1か所ではありません'
tpl = tpl.replace('UCHU_TEMPLATE', json.dumps(ut0, ensure_ascii=False).replace('</', '<\\/'))   # 宇宙の画面を index.html に入れる（ボタンで、いまのデータから別窓に組み立てる）
assert tpl.count('DEFAULT_DATA') == 1, 'app_template.html の DEFAULT_DATA が1か所ではありません'
(root / 'index.html').write_text(tpl.replace('DEFAULT_DATA', dump(data)), encoding='utf-8')
ver = re.search(r"APP_VERSION = '([^']+)'", tpl).group(1)

print(f'index.html を作りました（{ver}・わざ {len(data["nodes"])}・つながり {len(data["edges"])}）')
