from pathlib import Path
p=Path('arqcalc_webapp/views.py')
t=p.read_text(encoding='utf-8')
t=t.replace('cell = {"value": item.get(field, "")} #REMOVER', 'cell = {"name": field, "value": item.get(field, "")}  # now includes name')
t=t.replace('cell = {"value": item.get(field, "")}', 'cell = {"name": field, "value": item.get(field, "")}')
p.write_text(t, encoding='utf-8')
print('updated')
