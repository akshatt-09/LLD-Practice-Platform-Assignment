import React, {useEffect, useMemo, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {ArrowLeft, ArrowRight, CheckCircle2, ChevronRight, Clock3, Code2, History, Lightbulb, Play, Send, Sparkles, Target, XCircle} from 'lucide-react';
import './styles.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

function App(){
  const [problems,setProblems]=useState([]); const [attempts,setAttempts]=useState([]);
  const [screen,setScreen]=useState('home'); const [selected,setSelected]=useState(null); const [solution,setSolution]=useState(''); const [result,setResult]=useState(null); const [loading,setLoading]=useState(false); const [error,setError]=useState('');
  const refresh=()=>fetch(API+'/attempts').then(r=>r.json()).then(setAttempts).catch(()=>{});
  useEffect(()=>{fetch(API+'/problems').then(r=>r.json()).then(setProblems).catch(()=>setError('Backend is not running. Start Flask on port 5000.')); refresh()},[]);
  const openProblem=(p, initial='')=>{setSelected(p);setSolution(initial);setResult(null);setError('');setScreen('practice')};
  const submit=async()=>{if(solution.trim().length<30){setError('Write at least 30 characters so the evaluator has enough context.');return} setLoading(true);setError(''); try{const r=await fetch(API+'/attempts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({problem_id:selected.id,solution})}); const d=await r.json(); if(!r.ok) throw new Error(d.error||'Submission failed'); setResult(d); refresh(); setScreen('feedback')}catch(e){setError(e.message)}finally{setLoading(false)}};
  const latestByProblem=useMemo(()=>Object.fromEntries(attempts.map(a=>[a.problem_id,a])),[attempts]);
  return <div className="app">
    <header><div className="brand"><div className="brandmark">LL</div><div><strong>LLD Lab</strong><span>Practice platform</span></div></div><nav><button className={screen==='home'?'active':''} onClick={()=>setScreen('home')}>Problems</button><button className={screen==='history'?'active':''} onClick={()=>{refresh();setScreen('history')}}><History size={16}/> History</button></nav></header>
    <main>
      {screen==='home' && <Home problems={problems} latest={latestByProblem} onOpen={openProblem}/>} 
      {screen==='practice' && selected && <Practice p={selected} solution={solution} setSolution={setSolution} onBack={()=>setScreen('home')} onSubmit={submit} loading={loading} error={error}/>} 
      {screen==='feedback' && result && <Feedback result={result} onRetry={()=>openProblem(result.problem,result.solution)} onHistory={()=>{refresh();setScreen('history')}}/>}
      {screen==='history' && <HistoryView attempts={attempts} problems={problems} onOpen={openProblem} />}
    </main>
  </div>
}

function Home({problems,latest,onOpen}){return <>
  <section className="hero"><div><p className="eyebrow"><Sparkles size={15}/> DESIGN. SUBMIT. IMPROVE.</p><h1>Practice LLD like a real<br/><em>design review.</em></h1><p className="sub">Pick a problem, explain your design, submit an attempt, and get structured feedback on responsibilities, relationships, extensibility and trade-offs.</p></div><div className="hero-card"><Target size={20}/><div><b>Practice loop</b><span>Choose → Design → Submit → Feedback → Review → Try again</span></div></div></section>
  <section className="section-head"><div><p className="eyebrow">PROBLEM SET</p><h2>Choose a design problem</h2></div><span className="count">{problems.length} challenges</span></section>
  <div className="grid">{problems.map((p,i)=><article className="problem" key={p.id}><div className="number">0{i+1}</div><div className="tags"><span>{p.difficulty}</span><span><Clock3 size={13}/>{p.time}</span></div><h3>{p.title}</h3><p>{p.summary}</p><div className="card-bottom">{latest[p.id]?<span className="attempted">Last: {latest[p.id].score}/100</span>:<span className="new">Not attempted</span>}<button onClick={()=>onOpen(p)}>{latest[p.id]?'Try again':'Start'} <ChevronRight size={17}/></button></div></article>)}</div>
  <section className="how"><div><p className="eyebrow">WHAT MATTERS</p><h2>Feedback, not just a score.</h2></div><div className="principles"><span><Code2/> Domain modelling</span><span><Target/> Responsibility boundaries</span><span><Lightbulb/> Trade-offs & extensibility</span></div></section>
</>}

function Practice({p,solution,setSolution,onBack,onSubmit,loading,error}){return <section className="practice"><button className="back" onClick={onBack}><ArrowLeft size={17}/> All problems</button><div className="practice-head"><div><div className="tags"><span>{p.difficulty}</span><span><Clock3 size={13}/>{p.time}</span></div><h1>{p.title}</h1><p>{p.summary}</p></div><div className="step"><b>01</b><span>Design & submit</span></div></div><div className="workspace"><aside><h3>Requirements</h3><p className="aside-note">Treat these as the contract for your design.</p><ul>{p.requirements.map((x,i)=><li key={i}><span>{i+1}</span>{x}</li>)}</ul><div className="hint"><Lightbulb size={17}/><div><b>Think about</b>{p.hints.map((h,i)=><p key={i}>{h}</p>)}</div></div></aside><div className="editor"><div className="editor-top"><span>Your design</span><span>{solution.trim().split(/\s+/).filter(Boolean).length} words</span></div><textarea value={solution} onChange={e=>setSolution(e.target.value)} placeholder={'Example:\n\nclass ParkingLot\n- owns available spots\n- delegates pricing to PricingStrategy\n\nclass ParkingTicket\n- stores entry time and vehicle\n\nExplain relationships, key flows, edge cases and trade-offs...'} />{error&&<div className="error"><XCircle size={17}/>{error}</div>}<div className="editor-bottom"><span>Text is enough. Code or diagrams are optional.</span><button onClick={onSubmit} disabled={loading}>{loading?'Evaluating…':<>Submit attempt <Send size={16}/></>}</button></div></div></div></section>}

function Feedback({result,onRetry,onHistory}){const f=result.feedback;return <section className="feedback"><div className="feedback-top"><div><p className="eyebrow"><CheckCircle2 size={15}/> ATTEMPT SUBMITTED</p><h1>Review your design.</h1><p>{f.summary}</p></div><div className="score"><strong>{f.score}</strong><span>/ 100</span></div></div><div className="feedback-grid"><div className="panel"><h3>What worked</h3>{f.strengths.length?f.strengths.map((x,i)=><div className="feedback-row positive" key={i}><CheckCircle2 size={18}/><span>{x}</span></div>):<p className="muted">No strong signal detected yet. That's okay—use the improvements to revise.</p>}</div><div className="panel"><h3>Improve next</h3>{f.improvements.map((x,i)=><div className="feedback-row" key={i}><ArrowRight size={18}/><span>{x}</span></div>)}</div></div><div className="next"><div><b>Next step</b><span>{f.next_step}</span></div><div className="actions"><button className="secondary" onClick={onHistory}>View history</button><button onClick={onRetry}>Try again <ArrowRight size={16}/></button></div></div></section>}

function HistoryView({attempts,problems,onOpen}){return <section className="history"><div className="section-head"><div><p className="eyebrow">YOUR WORK</p><h1>Attempt history</h1><p className="sub">Use previous attempts to see whether your design improves over time.</p></div></div>{!attempts.length?<div className="empty"><History size={30}/><h3>No attempts yet</h3><p>Submit your first design and it will appear here.</p></div>:<div className="history-list">{attempts.map(a=>{const p=problems.find(x=>x.id===a.problem_id);return <div className="history-row" key={a.id}><div className="hist-num">#{a.id}</div><div className="hist-main"><b>{p?.title||a.problem_id}</b><span>{new Date(a.created_at).toLocaleString()}</span></div><div className="hist-score">{a.score}<small>/100</small></div><button onClick={()=>p&&onOpen(p,a.solution)}>Review <ArrowRight size={16}/></button></div>})}</div>}</section>}

createRoot(document.getElementById('root')).render(<App/>);
