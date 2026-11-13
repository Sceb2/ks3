from pathlib import Path
from urllib.parse import unquote
from html import escape
import json,re
from lxml import html

ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'data/year7-resources.json').read_text())
PLC=json.loads((ROOT/'data/y7-test1-plc.json').read_text())
DRAFT=(ROOT/'draft-y7-test-1-route-2.html').read_text()
old1=html.parse(str(ROOT/'year-7-test-1.html'))
draft_tree=html.fromstring(DRAFT)
for t in DATA['1']['topics']:
    slug={'Induction':'prior','Cells':'cells','Energy':'energy'}[t['title']]
    t['checklist']=draft_tree.xpath(f'//section[@id="{slug}"]//a[contains(@class,"checklist-link")]/@href')[0]
DATA['1']['test_checklist']=draft_tree.xpath('//section[@id="test"]//a[contains(@class,"checklist-link")]/@href')[0]
SMART={}
for a in old1.xpath('//a[contains(@href,"smart-bank")]'):
    if 'cell' in a.get('href'):SMART['cells']=a.get('href')
    if 'energy' in a.get('href'):SMART['energy']=a.get('href')

head=DRAFT[:DRAFT.index('</head>')+7]
head=head.replace('Year 7 Test 1 · Exam Bank draft','Year 7 Test 1 · Exam Bank')
head=head.replace('draft-assets/checklist-three-arrows.png','draft-assets/checklist-three-arrows.png')
head=head.replace('</head>','<style>.masthead{background:#07583e;border-bottom:0}.masthead h1,:root[data-theme=dark] .masthead h1{color:#fff;text-shadow:2px 2px 2px rgba(0,0,0,.65);flex:1;min-width:0}.masthead .header-back{color:#fff}.topic-link .topic-label{color:#07583e;font-size:1rem;font-weight:700;white-space:nowrap}:root[data-theme=dark] .topic-link .topic-label{color:#a0e7c1}@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .topic-link .topic-label{color:#a0e7c1}}@media(max-width:400px){.masthead h1,:root[data-page-view]:not([data-page-view=test]) .masthead h1,:root[data-page-view=test] .masthead h1{font-size:1.05rem}}</style></head>')
style=html.fromstring(DRAFT)
icons={}
for group in style.xpath('//section[contains(@class,"resource-group")][h3]'):
    title=group.xpath('string(./h3/span)').strip()
    if title and title not in icons:
        icons[title]=html.tostring(group.xpath('./h3/svg')[0],encoding='unicode',method='html')
ext_icon=html.tostring(style.xpath('//svg[contains(@class,"external-icon")]')[0],encoding='unicode',method='html')
check_img='<img class="checklist-illustration" src="draft-assets/checklist-three-arrows.png" alt="" width="96" height="80">'

def link(a,cls='resource-row',pack=False):
    title=escape(a['title'].replace('Open question pack','').strip())
    href=escape(a['href'],quote=True)
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener noreferrer"><span>{title}</span>{ext_icon}<span class="sr-only"> (opens in a new tab)</span></a>'

def checklist(href,plc=None):
    content=f'{check_img}<span><strong>Start with the checklist</strong><small>Check what you need to revise</small></span>'
    if plc:return f'<button class="checklist-link" type="button" data-plc="{plc}" aria-haspopup="dialog">{content}</button>'
    return f'<a class="checklist-link" href="{escape(href,quote=True)}" target="_blank" rel="noopener noreferrer">{content}<span class="sr-only"> (opens in a new tab)</span></a>'

def group(title,note,items):
    if not items:return ''
    return f'<section class="resource-group"><h3>{icons[title]}<span>{title}</span></h3><p class="group-note">{note}</p><div class="resource-list">'+''.join(link(a) for a in items)+'</div></section>'

def questions(levels):
    if not any(levels.values()):return ''
    inner=''
    for name in ('developing','secure','extending'):
        items=levels.get(name,[])
        if items:inner+=f'<details class="level"><summary>{name.title()}</summary><div class="resource-list">'+''.join(link(a,pack=True) for a in items)+'</div></details>'
    return f'<section class="resource-group"><h3>{icons["Exam-style questions"]}<span>Exam-style questions</span></h3><p class="group-note">Choose a level, then a question pack.</p>{inner}</section>'

def slug_for(title,used):
    base=title.lower().replace('revision: ','revision-')
    base=re.sub(r'[^a-z0-9]+','-',base).strip('-')
    slug=base
    n=2
    while slug in used:slug=f'{base}-{n}';n+=1
    used.add(slug)
    return slug

def topics_view(i):
    test=DATA[str(i)];used=set();rows=[];sections=[];mapping={}
    for n,t in enumerate(test['topics'],1):
        slug=slug_for(t['title'],used)
        if i==1 and t['title']=='Induction':slug='prior'
        mapping[slug]=t['title']
        rows.append(f'<a class="topic-link" href="#{slug}"><span class="topic-number" aria-hidden="true">{n}</span><span class="topic-label">{escape(t["title"])}</span></a>')
        smart=[]
        if i==1 and slug in SMART:smart=[{'title':'Cell Structure' if slug=='cells' else 'Energy Stores and Transfers','href':SMART[slug]}]
        res=group('Smart Bank','Learn in short chunks, then check understanding.',smart)
        res+=group('Knowledge organisers','Review key facts, then recall from memory.',t['knowledge'])
        res+=group('Multiple-choice quizzes','Answer quick questions and check your understanding.',t['quizzes'])
        res+=questions(t['questions'])
        if t['other']:
            res+='<details class="extra-links"><summary>Other resources <span>Videos and websites</span></summary><div class="resource-list">'+''.join(link(a) for a in t['other'])+'</div></details>'
        sections.append(f'<section class="view topic-view" data-view="{slug}" id="{slug}" aria-labelledby="{slug}-title" hidden><div class="topic-heading"><h2 class="sr-only" id="{slug}-title" tabindex="-1">{escape(t["title"])}</h2>{checklist(t["checklist"],slug if i==1 else None)}</div>{res}</section>')
    tips='<details class="tips"><summary>How should I revise?</summary><ol class="revision-journey"><li><strong>Check</strong><span>Use your checklist to choose what to revise.</span></li><li><strong>Learn</strong><span>Read a knowledge organiser or use a Smart Bank.</span></li><li><strong>Recall</strong><span>Test what you remember without looking.</span></li><li><strong>Practise</strong><span>Try a quiz or exam-style question pack.</span></li><li><strong>Review</strong><span>Go back to anything you found difficult.</span></li></ol></details>'
    test_view=f'<section class="view" data-view="test" id="test" aria-labelledby="test-title"><h2 class="sr-only" id="test-title" tabindex="-1">Test {i} topics</h2>{checklist(test["test_checklist"],'test' if i==1 else None)}<nav class="topic-list" aria-label="Test {i} topics">'+''.join(rows)+'</nav>'+tips+'</section>'
    return test_view+''.join(sections),mapping

def script(i,mapping):
    names=json.dumps(mapping,ensure_ascii=False)
    return f'''<script>(()=>{{const views=[...document.querySelectorAll('[data-view]')],ids=new Set(views.map(v=>v.dataset.view)),names={names};function show(focus){{let id=decodeURIComponent(location.hash.slice(1));if(!ids.has(id))id='test';for(const v of views)v.hidden=v.dataset.view!==id;document.documentElement.dataset.pageView=id;document.querySelector('.footer-back').hidden=id==='test';document.querySelector('.masthead h1').textContent=id==='test'?'Test {i}':'Test {i}: '+names[id];const back=document.querySelector('.header-back');back.href=id==='test'?'index.html':'#test';back.textContent=id==='test'?'← Back to Year 7':'← Back to topics';document.title=(id==='test'?'Year 7 Test {i}':'Test {i}: '+names[id])+' · Exam Bank';if(focus){{const h=document.getElementById(id+'-title');if(h)h.focus({{preventScroll:true}});window.scrollTo(0,0)}}}}window.addEventListener('hashchange',()=>show(true));show(false);const b=document.getElementById('theme'),root=document.documentElement,key='smart-bank-y7-hub-theme',media=matchMedia('(prefers-color-scheme: dark)');let mode='system';try{{let x=localStorage.getItem(key);if(x==='dark'||x==='light')mode=x}}catch(e){{}}function render(){{if(mode==='system')delete root.dataset.theme;else root.dataset.theme=mode;let dark=mode==='dark'||(mode==='system'&&media.matches);b.setAttribute('aria-pressed',String(dark));b.textContent=dark?'Light mode':'Dark mode'}}b.addEventListener('click',()=>{{let dark=mode==='dark'||(mode==='system'&&media.matches);mode=dark?'light':'dark';try{{localStorage.setItem(key,mode)}}catch(e){{}}render()}});if(media.addEventListener)media.addEventListener('change',()=>{{if(mode==='system')render()}});render()}})();</script>'''

for i in range(1,6):
    content,names=topics_view(i)
    page=head.replace('Year 7 Test 1 · Exam Bank',f'Year 7 Test {i} · Exam Bank')
    if i==1:page=page.replace('</head>','<style>'+ (ROOT/'assets/plc.css').read_text() +'</style></head>')
    modal='';extra_scripts=''
    if i==1:
        modal='''<dialog class="plc-dialog" id="plc-dialog" aria-labelledby="plc-title"><div class="plc-toolbar"><button class="plc-action" id="plc-print" type="button">Print a copy</button><button class="plc-close" id="plc-close" type="button" aria-label="Close checklist">×</button></div><div class="plc-body"><h2 id="plc-title">Checklist</h2><p class="plc-intro">Choose red, amber or green for each learning outcome.</p><table class="plc-table"><thead><tr><th scope="col">Learning outcome</th><th scope="col">My RAG rating</th></tr></thead><tbody id="plc-table-body"></tbody></table><div class="plc-footer"><a id="plc-original" href="#" target="_blank" rel="noopener noreferrer">Open the original PDF <span class="sr-only">(opens in a new tab)</span></a><button class="plc-reset" id="plc-reset" type="button">Clear my ratings</button></div></div></dialog>'''
        data_json=json.dumps(PLC,ensure_ascii=False).replace('<','\\u003c')
        extra_scripts='<script id="plc-data" type="application/json">'+data_json+'</script><script src="assets/jspdf.umd.min.js"></script><script src="assets/plc.js"></script>'
    page+=f'<body><a class="skip" href="#main">Skip to resources</a><div class="page"><header class="masthead"><h1>Test {i}</h1><a class="header-back" href="index.html">← Back to Year 7</a></header><main id="main" class="main" tabindex="-1">{content}</main><footer class="footer"><a class="footer-back" href="#test" hidden>← Back to topics</a><a class="feedback-link" href="mailto:wormstonel@crispins.co.uk">Got feedback? Email Mr Wormstone</a><button class="theme" id="theme" type="button" aria-pressed="false">Dark mode</button></footer></div>{modal}{script(i,names)}{extra_scripts}</body></html>'
    (ROOT/f'year-7-test-{i}.html').write_text(page)

# A year hub follows the same type, colour and numbered navigation as its test pages.
months={1:'October',2:'December',3:'February',4:'March',5:'July'}
rows=[]
for i in range(1,6):
    topic_names=', '.join(t['title'] for t in DATA[str(i)]['topics'])
    rows.append(f'<a class="topic-link year-test-link" href="year-7-test-{i}.html"><span class="topic-number">Test {i}</span><span class="topic-label">{months[i]} – {escape(topic_names)}</span></a>')
index_head=head.replace('Year 7 Test 1 · Exam Bank','Year 7 Science · Exam Bank').replace('</head>','<style>.year-test-link{min-height:66px;gap:12px}.year-test-link .topic-number{width:85px;letter-spacing:-.03em;font-size:1.08rem;font-style:italic;white-space:nowrap;transform:none}.year-test-link .topic-label{min-width:0;overflow-x:auto;scrollbar-width:thin;white-space:nowrap;font-size:1rem;font-weight:700;color:#07583e}.year-intro{color:var(--muted);margin:0 0 20px}.year-hub .topic-list{margin-top:0}.year-hub .topic-link{font-size:1rem}.masthead h1{font-size:1.4rem}@media(max-width:400px){.year-test-link .topic-number{width:74px;font-size:.96rem}.year-test-link .topic-label{font-size:.9rem}}</style></head>')
index=f'''{index_head}<body><a class="skip" href="#main">Skip to tests</a><div class="page"><header class="masthead"><h1>Year 7 Science</h1></header><main id="main" class="main year-hub" tabindex="-1"><p class="year-intro">Choose your test to find its checklists, revision resources and practice questions.</p><nav class="topic-list" aria-label="Year 7 tests">{''.join(rows)}</nav><details class="tips"><summary>How will I be assessed?</summary><p>You will have five tests this year. Each test includes questions from that term and previous topics.</p></details></main><footer class="footer"><a class="feedback-link" href="mailto:wormstonel@crispins.co.uk">Got feedback? Email Mr Wormstone</a><button class="theme" id="theme" type="button" aria-pressed="false">Dark mode</button></footer></div><script>(()=>{{const b=document.getElementById('theme'),root=document.documentElement,key='smart-bank-y7-hub-theme',media=matchMedia('(prefers-color-scheme: dark)');let mode='system';try{{let x=localStorage.getItem(key);if(x==='dark'||x==='light')mode=x}}catch(e){{}}function render(){{if(mode==='system')delete root.dataset.theme;else root.dataset.theme=mode;let dark=mode==='dark'||(mode==='system'&&media.matches);b.setAttribute('aria-pressed',String(dark));b.textContent=dark?'Light mode':'Dark mode'}}b.addEventListener('click',()=>{{let dark=mode==='dark'||(mode==='system'&&media.matches);mode=dark?'light':'dark';try{{localStorage.setItem(key,mode)}}catch(e){{}}render()}});if(media.addEventListener)media.addEventListener('change',()=>{{if(mode==='system')render()}});render()}})();</script></body></html>'''
(ROOT/'index.html').write_text(index)
print('Built Year 7 index and five tests')
