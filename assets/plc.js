(()=>{
  const data=JSON.parse(document.getElementById('plc-data').content.textContent);
  const dialog=document.getElementById('plc-dialog');
  const title=document.getElementById('plc-title');
  const table=document.getElementById('plc-table-body');
  const source=document.getElementById('plc-original');
  const storagePrefix='y7-test1-plc-';
  let currentKey=null, outcomes=[], values=[];
  const read=key=>{try{return JSON.parse(sessionStorage.getItem(storagePrefix+key))||[]}catch{return []}};
  const save=()=>{try{sessionStorage.setItem(storagePrefix+currentKey,JSON.stringify(values))}catch{}};
  function open(key){
    const item=data[key];if(!item)return;
    currentKey=key;outcomes=[];values=read(key);table.replaceChildren();
    title.textContent=key==='test'?'Test 1 checklist':'Test 1: '+Object.keys(item.sections)[0]+' checklist';
    source.href=item.pdf;
    for(const [section,rows] of Object.entries(item.sections)){
      const heading=document.createElement('tr');heading.className='plc-section';const th=document.createElement('th');th.colSpan=2;th.textContent=section;heading.append(th);table.append(heading);
      for(const outcome of rows){
        const index=outcomes.length;outcomes.push({section,text:outcome});
        const tr=document.createElement('tr');tr.className='plc-item';tr.dataset.state=values[index]||'';
        const td=document.createElement('td');td.className='plc-outcome';td.textContent=outcome;
        const rating=document.createElement('td');rating.className='plc-rating';
        const choices=document.createElement('div');choices.className='plc-choices';choices.setAttribute('role','radiogroup');choices.setAttribute('aria-label',outcome);
        for(const [letter,name] of [['R','Red'],['A','Amber'],['G','Green']]){
          const label=document.createElement('label');label.className='plc-choice '+letter.toLowerCase();
          const input=document.createElement('input');input.type='radio';input.name='plc-'+index;input.value=letter;input.checked=values[index]===letter;input.setAttribute('aria-label',name);
          input.addEventListener('change',()=>{values[index]=letter;tr.dataset.state=letter;save()});
          label.append(input,document.createTextNode(letter));choices.append(label);
        }
        rating.append(choices);tr.append(td,rating);table.append(tr);
      }
    }
    dialog.showModal();
    document.getElementById('plc-close').focus();
  }
  document.querySelectorAll('button[data-plc]').forEach(button=>{button.disabled=false;button.addEventListener('click',()=>open(button.dataset.plc))});
  document.getElementById('plc-close').addEventListener('click',()=>dialog.close());
  document.getElementById('plc-reset').addEventListener('click',()=>{values=[];save();table.querySelectorAll('.plc-item').forEach(row=>{row.dataset.state='';row.querySelectorAll('input').forEach(input=>input.checked=false)})});
  document.getElementById('plc-print').addEventListener('click',()=>{
    const popup=window.open('','_blank');if(!popup){alert('Please allow pop-ups to open the PDF copy.');return}
    popup.document.write('<title>Preparing checklist PDF</title><p>Preparing your PDF copy…</p>');
    try{
      const pdf=new window.jspdf.jsPDF({unit:'mm',format:'a4'});
      const label=title.textContent;let y=0,page=0;
      function newPage(){if(page)pdf.addPage();page++;pdf.setFont('helvetica','bold');pdf.setFontSize(15);pdf.setTextColor(7,88,62);pdf.text(label,15,19);pdf.setDrawColor(7,88,62);pdf.line(15,23,195,23);pdf.setFontSize(9);pdf.setTextColor(55,72,62);pdf.text('My RAG ratings',15,29);y=36}
      newPage();let lastSection='';
      for(let i=0;i<outcomes.length;i++){
        const o=outcomes[i];const lines=pdf.splitTextToSize(o.text,156);const h=Math.max(10,lines.length*4.5+4);
        if(y+h+10>280){newPage();lastSection=''}
        if(o.section!==lastSection){if(y+10+h>280)newPage();pdf.setFillColor(232,244,237);pdf.rect(15,y,180,8,'F');pdf.setTextColor(7,88,62);pdf.setFont('helvetica','bold');pdf.setFontSize(10);pdf.text(o.section,18,y+5.5);y+=10;lastSection=o.section}
        const state=values[i]||'';const colors={R:[255,225,220],A:[255,240,190],G:[220,243,225]};const bg=colors[state]||[245,247,245];
        pdf.setFillColor(...bg);pdf.rect(181,y,14,h,'F');pdf.setDrawColor(207,218,209);pdf.line(15,y+h,195,y+h);
        pdf.setTextColor(24,49,39);pdf.setFont('helvetica','normal');pdf.setFontSize(9);pdf.text(lines,18,y+5.5);
        pdf.setFont('helvetica','bold');pdf.text(state||'-',188,y+6,{align:'center'});y+=h;
      }
      const count=pdf.internal.getNumberOfPages();for(let n=1;n<=count;n++){pdf.setPage(n);pdf.setFontSize(8);pdf.setTextColor(100,110,103);pdf.text('Page '+n+' of '+count,195,290,{align:'right'})}
      popup.location.replace(URL.createObjectURL(pdf.output('blob')));
    }catch(error){popup.document.body.textContent='Could not create the PDF copy. Please use the original PDF link below.';console.error(error)}
  });
})();
