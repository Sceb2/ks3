from lxml import html
from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parent.parent

def label(a):
    return ''.join(a.xpath('./text()')).strip() or ' '.join(a.xpath('.//text()[not(ancestor::*[contains(@class,"sr-only")]) and not(ancestor::*[contains(@class,"arrow")])]')).strip()

def links(section):
    return [{'title':label(a),'href':a.get('href')} for a in section.xpath('.//a[@href]')]

out={}
for i in range(1,6):
    # Reproduce the legacy link inventory from the pre-redesign commit.
    source=subprocess.check_output(['git','show',f'24884d1:year-7-test-{i}.html'],cwd=ROOT)
    d=html.fromstring(source)
    whole=d.xpath('(//a[contains(@href,"/Checklists/") and not(ancestor::details[contains(@class,"topic")])])[1]')
    topics=[]
    for topic in d.xpath('//details[contains(concat(" ",normalize-space(@class)," ")," topic ")][summary/h2]'):
        title=topic.xpath('string(./summary/h2)').strip()
        check=topic.xpath('.//a[contains(@class,"checklist-tile")][1]')
        groups={}
        for sec in topic.xpath('.//section[contains(@class,"tile-group")]'):
            heading=sec.xpath('string(./h3)').strip().lower()
            if 'knowledge' in heading:groups['knowledge']=links(sec)
            elif 'multiple' in heading:groups['quizzes']=links(sec)
        levels={}
        for lev in topic.xpath('.//details[contains(@class,"pack-level")]'):
            name=lev.xpath('string(./summary)').replace('question packs','').strip().lower()
            levels[name]=links(lev)
        other=topic.xpath('.//section[contains(@class,"other-resources")]')
        topics.append({'title':title,'checklist':check[0].get('href') if check else None,'knowledge':groups.get('knowledge',[]),'quizzes':groups.get('quizzes',[]),'questions':levels,'other':links(other[0]) if other else []})
    out[str(i)]={'test_checklist':whole[0].get('href') if whole else None,'topics':topics}
(ROOT/'data/year7-resources.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
for i,test in out.items():print(i,test['test_checklist'],[(t['title'],len(t['knowledge']),len(t['quizzes']),sum(map(len,t['questions'].values())),len(t['other'])) for t in test['topics']])
