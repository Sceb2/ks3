"""Extract the actual Y7 Term 1 checklist learning outcomes from supplied PDFs."""
from pathlib import Path
import subprocess,re,json
ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'resources/Checklists/Term 1'
FILES={'test':'Y7 Term 1 Checklist.pdf','prior':'Y7 Term 1 Induction Checklist.pdf','cells':'Y7 Term 1 Cells Checklist.pdf','energy':'Y7 Term 1 Energy Checklist.pdf'}
VERBS=('Link','Show','Use','Recognise','Identify','Explain','Describe','Draw','Compare','Define','Label','Order','State','Give','Sequence','Name','Calculate')

def extract(filename):
    raw=subprocess.check_output(['pdftotext','-layout',str(BASE/filename),'-']).decode()
    groups={};current=None
    for line in raw.splitlines():
        line=line.strip()
        if not line or line.startswith(('Topic','RAG Yourself')) or re.fullmatch(r'1\s+2',line):continue
        m=re.match(r'^(Y6 Induction|Cells|Energy)\s+(.+)$',line)
        if m:
            current={'Y6 Induction':'Induction','Cells':'Cells','Energy':'Energy'}[m.group(1)]
            line=m.group(2)
        if current is None:continue
        entries=groups.setdefault(current,[])
        if line.startswith(VERBS):entries.append(line)
        elif entries:entries[-1]+=' '+line
    return groups

out={key:{'pdf':'resources/Checklists/Term%201/'+filename.replace(' ','%20'),'sections':extract(filename)} for key,filename in FILES.items()}
(ROOT/'data/y7-test1-plc.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
for key,val in out.items():print(key,{k:len(v) for k,v in val['sections'].items()})
