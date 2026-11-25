"""index.html（ツリー）と uchu.html（概念宇宙）を、data/core_data.json から作る。
使い方: python3 build.py
- index.html：src/app_template.html に core_data.json をそのまま埋め込む
- uchu.html ：src/uchu_template.html に、core_data.json から作った宇宙用のグラフを埋め込む
"""
import json, pathlib, re, datetime
root = pathlib.Path(__file__).resolve().parent
data = json.loads((root / 'data' / 'core_data.json').read_text(encoding='utf-8'))
dump = lambda o: json.dumps(o, ensure_ascii=False, indent=1).replace('</', '<\\/')

# ツリー
tpl = (root / 'src' / 'app_template.html').read_text(encoding='utf-8')
assert tpl.count('DEFAULT_DATA') == 1, 'app_template.html の DEFAULT_DATA が1か所ではありません'
(root / 'index.html').write_text(tpl.replace('DEFAULT_DATA', dump(data)), encoding='utf-8')
ver = re.search(r"APP_VERSION = '([^']+)'", tpl).group(1)

# 概念宇宙：銀河（ことば・そうさ・説明・文学）、根拠の引用（概念の根拠／n段階）、そうさの使用を足す
def galaxy(n):
    return 'kotoba' if n['axis'] == 'k' else 'sosa' if n['axis'] == 'n' else (n.get('tree') or 'setsumei')
def source_refs(n):
    m = {}
    def add(i, w):
        m.setdefault(i, [])
        if w not in m[i]: m[i].append(w)
    for r in n.get('basis_refs') or []: add(r, '概念の根拠')
    for st in n.get('stages') or []:
        for r in st.get('basis_refs') or []: add(r, f"{st['band']}段階")
    return [{'id': k, 'where': sorted(v, key=lambda w: (w == '概念の根拠', w))} for k, v in m.items()]
nodes = [{**n, 'galaxy': galaxy(n), 'source_refs': source_refs(n)} for n in data['nodes']]
tool_uses = [{'from': n['id'], 'to': t['id']} for n in data['nodes'] for t in (n.get('tools') or [])]
today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y.%m.%d')
graph = {'nodes': nodes, 'edges': data['edges'], 'toolUses': tool_uses, 'trees': data['trees'],
         'source': {'version': ver, 'nodeCount': len(nodes), 'edgeCount': len(data['edges']), 'toolUseCount': len(tool_uses), 'based_on': 'data/core_data.json', 'viewer_updated': today},
         'refs': data['refs'], 'lits': data['lits']}
ut = (root / 'src' / 'uchu_template.html').read_text(encoding='utf-8')
assert ut.count('GRAPH_DATA') == 1, 'uchu_template.html の GRAPH_DATA が1か所ではありません'
ut = ut.replace('__VER__', ver).replace('__DATE__', today)
(root / 'uchu.html').write_text(ut.replace('GRAPH_DATA', json.dumps(graph, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')), encoding='utf-8')
print(f'index.html と uchu.html を作りました（{ver}・わざ {len(nodes)}・つながり {len(data["edges"])}・そうさの使用 {len(tool_uses)}）')
