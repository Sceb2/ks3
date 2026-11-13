"""Extract the linked Year 7 PLC outcomes from their source PDFs."""
from pathlib import Path
from urllib.parse import unquote
import subprocess,re,json
ROOT=Path(__file__).resolve().parent.parent
RESOURCES=json.loads((ROOT/'data/year7-resources.json').read_text())
TEST1=json.loads((ROOT/'data/y7-test1-plc.json').read_text())
VERBS=('Link','Show','Use','Recognise','Identify','Explain','Describe','Draw','Compare','Define','Label','Order','State','Give','Sequence','Name','Calculate','Suggest','List','Write','Predict','Evaluate','Design','Make','Measure','Construct','Interpret','Balance','Classify','Know','Recall','Plan','Apply','Determine','Estimate','Model','Find','Observe','Read','Outline','Match','Try','Create','Discuss','Convert')
TOPIC=re.compile(r'^(Y6 Induction|Cells|Energy|Chemicals|Forces and|Forces|Motion|Interdependence|Electricity)\s+(.+)$')
LABEL={'Y6 Induction':'Induction','Forces and':'Forces and Motion','Motion':'Forces and Motion','Forces':'Forces'}

def extract(href):
    file=ROOT/unquote(href)
    raw=subprocess.check_output(['pdftotext','-layout',str(file),'-']).decode()
    groups={};current=None
    for original in raw.splitlines():
        line=original.strip()
        if not line or line.startswith(('Topic','RAG','Learning Outcomes')) or re.fullmatch(r'1\s+2',line):continue
        m=TOPIC.match(line)
        if m:
            current=LABEL.get(m.group(1),m.group(1))
            line=m.group(2)
        if current is None:continue
        entries=groups.setdefault(current,[])
        if line.lstrip('"“').startswith(VERBS):entries.append(line.strip('"'))
        elif entries:entries[-1]+=' '+line
    return groups

def slug(title):
    title=title.lower().replace('revision: ','revision-')
    title=re.sub(r'[^a-z0-9]+','-',title).strip('-')
    return 'prior' if title=='induction' else title

out={}
for i,test in RESOURCES.items():
    whole=test['test_checklist'] or TEST1['test']['pdf']
    entries={'test':{'pdf':whole,'title':f'Test {i} checklist','sections':extract(whole)}}
    for t in test['topics']:
        key=slug(t['title'])
        href=TEST1[key]['pdf'] if i=='1' else t['checklist']
        if not href:raise ValueError((i,t['title']))
        display=re.sub(r'^Revision:\s*(.+)$',r'\1 (Revision)',t['title'])
        entries[key]={'pdf':href,'title':f'Test {i}: {display} checklist','sections':extract(href)}
    out[i]=entries
    print('Test',i,[(k,sum(map(len,v['sections'].values()))) for k,v in entries.items()])
(ROOT/'data/year7-plc.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
