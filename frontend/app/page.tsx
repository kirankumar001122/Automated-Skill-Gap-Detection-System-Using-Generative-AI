'use client'

import { useState, useEffect, useRef } from 'react'
import { 
  Bot, 
  Code2, 
  Terminal, 
  Settings, 
  Play, 
  Bug, 
  Zap, 
  Info, 
  CheckCircle2, 
  XCircle, 
  Loader2, 
  ChevronRight,
  LayoutDashboard,
  MessageSquare,
  Activity,
  Trash2,
  Share2,
  Github
} from 'lucide-react'
import CodeEditor from './components/CodeEditor'
import AgentStatus from './components/AgentStatus'
import OutputConsole from './components/OutputConsole'
import LiveConsole from './components/LiveConsole'
import { generateCode, runCode, debugCode, optimizeCode, explainCode } from './services/api'

const LANGUAGES = [
  { value: 'python', label: 'Python', icon: '🐍', color: 'text-yellow-400' },
  { value: 'java', label: 'Java', icon: '☕', color: 'text-red-500' },
  { value: 'javascript', label: 'JavaScript', icon: '📜', color: 'text-yellow-300' },
  { value: 'cpp', label: 'C++', icon: '⚙️', color: 'text-blue-500' },
  { value: 'c', label: 'C', icon: '🔧', color: 'text-gray-400' }
]

export default function Home() {
  const [prompt, setPrompt] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('python')
  const [generatedCode, setGeneratedCode] = useState('')
  const [output, setOutput] = useState('')
  const [agentTasks, setAgentTasks] = useState<any[]>([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [consoleMessages, setConsoleMessages] = useState<Array<{type: string, message: string}>>([])
  const [activeTab, setActiveTab] = useState('editor') // editor, explanation
  const [explanation, setExplanation] = useState('')
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [consoleMessages])

  const addConsoleMessage = (type: string, message: string) => {
    setConsoleMessages(prev => [...prev, { type, message }])
  }

  const handleAction = async (actionType: 'generate' | 'run' | 'debug' | 'optimize' | 'explain') => {
    if (actionType === 'generate' && !prompt.trim()) return
    if (actionType !== 'generate' && !generatedCode.trim()) return

    setIsProcessing(true)
    if (actionType === 'generate') {
      setGeneratedCode('')
      setOutput('')
      setAgentTasks([])
      setExplanation('')
      setConsoleMessages([])
      addConsoleMessage('info', `🚀 Initializing Multi-Agent System for ${selectedLanguage}...`)
    }

    try {
      let response: any
      switch (actionType) {
        case 'generate':
          let autoLang = selectedLanguage
          const lowerPrompt = prompt.toLowerCase()
          if (lowerPrompt.includes('python')) autoLang = 'python'
          else if (lowerPrompt.includes('java ') || lowerPrompt.includes('java,') || lowerPrompt.endsWith('java')) autoLang = 'java'
          else if (lowerPrompt.includes('javascript') || lowerPrompt.includes('js ')) autoLang = 'javascript'
          else if (lowerPrompt.includes('c++') || lowerPrompt.includes('cpp')) autoLang = 'cpp'
          else if (lowerPrompt.includes(' c ') || lowerPrompt.endsWith(' c')) autoLang = 'c'
          
          if (autoLang !== selectedLanguage) {
            setSelectedLanguage(autoLang)
            addConsoleMessage('info', `🤖 Auto-detected language: ${autoLang.toUpperCase()}`)
          }
          
          response = await generateCode({ prompt, language: autoLang })
          if (response.generated_code) setGeneratedCode(response.generated_code)
          if (response.execution_result) setOutput(response.execution_result.output || response.execution_result.error || '')
          if (response.explanation) setExplanation(response.explanation)
          if (response.agent_tasks) setAgentTasks(response.agent_tasks)
          addConsoleMessage('success', '✅ Agent workflow completed successfully.')
          break
        case 'run':
          const requiresInput = /input\(|Scanner|System\.in\.read|BufferedReader|cin|scanf|gets|fgets|readline|prompt\(/i.test(generatedCode)
         let programInput: string | null | undefined = undefined;
          if (requiresInput) {
            programInput = window.prompt("The code appears to require user input. Enter input data for execution (or leave empty):")
            if (programInput === null) {
              addConsoleMessage('info', 'Execution cancelled by user.')
              setIsProcessing(false)
              return
            }
          }
          addConsoleMessage('info', `▶ Executing code on local system...`)
          setOutput('Running...')
          try {
            response = await runCode(generatedCode, selectedLanguage, programInput || undefined)
            
            let finalOutput = ''
            if (programInput) {
                finalOutput += `--- User Input ---\n${programInput}\n\n`
            }
            finalOutput += response.output || response.error || 'No output'
            
            setOutput(finalOutput)
            addConsoleMessage(response.success ? 'success' : 'error', response.success ? `✅ Execution completed in ${response.execution_time}s.` : `❌ Execution failed: ${response.status}`)
          } catch (e: any) {
            setOutput(`Execution error: ${e.message}`)
            addConsoleMessage('error', `❌ Execution error: ${e.message}`)
          }
          break
        case 'debug':
          addConsoleMessage('info', '🔍 Debug agent analyzing code...')
          response = await debugCode(generatedCode, selectedLanguage)
          if (response.generated_code) setGeneratedCode(response.generated_code)
          addConsoleMessage('success', '✅ Debugging phase complete.')
          break
        case 'optimize':
          addConsoleMessage('info', '⚡ Optimization agent improving code...')
          response = await optimizeCode(generatedCode, selectedLanguage)
          if (response.generated_code) setGeneratedCode(response.generated_code)
          addConsoleMessage('success', '✅ Code optimization complete.')
          break
        case 'explain':
          addConsoleMessage('info', '📝 Explanation agent generating docs...')
          response = await explainCode(generatedCode, selectedLanguage)
          if (response.explanation) {
            setExplanation(response.explanation)
            setActiveTab('explanation')
          }
          addConsoleMessage('success', '✅ Explanation generated.')
          break
      }
    } catch (error: any) {
      addConsoleMessage('error', `❌ Error: ${error.message}`)
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="flex h-screen w-full bg-slate-950 text-slate-200 overflow-hidden font-sans">
      {/* Dynamic Background Effect */}
      <div className="fixed inset-0 bg-grid pointer-events-none opacity-20" />
      <div className="fixed inset-0 bg-radial-gradient pointer-events-none" />

      {/* Sidebar */}
      <aside className={`transition-all duration-500 ease-in-out border-r border-white/5 bg-slate-950/80 backdrop-blur-2xl flex flex-col z-40 ${isSidebarOpen ? 'w-80' : 'w-0 overflow-hidden opacity-0'}`}>
        <div className="p-8 flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500 via-blue-600 to-cyan-400 flex items-center justify-center shadow-[0_0_20px_rgba(37,99,235,0.4)] ring-1 ring-white/30 group-hover:scale-105 transition-transform duration-500">
            <Bot className="w-7 h-7 text-white drop-shadow-[0_0_8px_rgba(255,255,255,0.5)]" />
          </div>
          <div>
            <h1 className="font-black text-xl tracking-tight text-white flex items-center">
              Nexora <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-300 text-xs font-black align-top ml-1">AI</span>
            </h1>
            <p className="text-[9px] uppercase tracking-[0.2em] text-slate-500 font-black leading-none mt-1">AI Autonomous Coding Workspace</p>
          </div>
        </div>

        <nav className="flex-1 px-6 space-y-8 overflow-y-auto pb-10">
          <div>
            <p className="px-2 mb-4 text-[11px] font-black text-slate-600 uppercase tracking-widest flex items-center gap-2">
              <Settings className="w-3 h-3" /> Environments
            </p>
            <div className="space-y-1.5">
              {LANGUAGES.map((lang) => (
                <button
                  key={lang.value}
                  onClick={() => setSelectedLanguage(lang.value)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm transition-all group ${
                    selectedLanguage === lang.value 
                      ? 'bg-blue-600/10 text-white border border-blue-500/20' 
                      : 'hover:bg-white/5 text-slate-400'
                  }`}
                >
                  <span className={`text-lg grayscale group-hover:grayscale-0 transition-all ${selectedLanguage === lang.value ? 'grayscale-0' : ''}`}>{lang.icon}</span>
                  <span className="font-semibold">{lang.label}</span>
                  {selectedLanguage === lang.value && (
                    <div className="ml-auto flex items-center gap-1.5">
                      <div className="w-1.5 h-1.5 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]" />
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>

          <div>
            <p className="px-2 mb-4 text-[11px] font-black text-slate-600 uppercase tracking-widest flex items-center gap-2">
              <Zap className="w-3 h-3" /> Core Actions
            </p>
            <div className="grid grid-cols-2 gap-3 px-1">
              <button onClick={() => handleAction('debug')} className="glass-card p-4 rounded-2xl flex flex-col items-center gap-2 group relative overflow-hidden">
                <div className="absolute inset-0 bg-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                <Bug className="w-5 h-5 text-orange-400 group-hover:scale-110 transition-transform" />
                <span className="text-[11px] font-bold uppercase tracking-tight">Debug</span>
              </button>
              <button onClick={() => handleAction('optimize')} className="glass-card p-4 rounded-2xl flex flex-col items-center gap-2 group relative overflow-hidden">
                <div className="absolute inset-0 bg-emerald-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                <Zap className="w-5 h-5 text-emerald-400 group-hover:scale-110 transition-transform" />
                <span className="text-[11px] font-bold uppercase tracking-tight">Optimize</span>
              </button>
              <button onClick={() => handleAction('explain')} className="glass-card p-4 rounded-2xl flex flex-col items-center gap-2 group relative overflow-hidden">
                <div className="absolute inset-0 bg-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                <Info className="w-5 h-5 text-blue-400 group-hover:scale-110 transition-transform" />
                <span className="text-[11px] font-bold uppercase tracking-tight">Explain</span>
              </button>
              <button onClick={() => {setGeneratedCode(''); setOutput(''); setExplanation(''); setAgentTasks([]);}} className="glass-card p-4 rounded-2xl flex flex-col items-center gap-2 group relative overflow-hidden">
                <div className="absolute inset-0 bg-rose-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                <Trash2 className="w-5 h-5 text-rose-400 group-hover:scale-110 transition-transform" />
                <span className="text-[11px] font-bold uppercase tracking-tight">Clear</span>
              </button>
            </div>
          </div>
        </nav>

        <div className="p-6 border-t border-white/5 bg-slate-900/40">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]" />
              <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Local Engine Active</span>
            </div>
          </div>
          <div className="p-3 rounded-xl bg-white/5 border border-white/5 flex items-center gap-3">
             <Activity className="w-4 h-4 text-blue-500" />
             <div className="flex-1">
               <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                 <div className="h-full bg-blue-500 w-full animate-pulse" />
               </div>
               <p className="text-[9px] mt-1.5 font-bold text-slate-500 uppercase tracking-tighter">System Health: Optimal</p>
             </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col relative overflow-hidden bg-transparent">
        {/* Top Sticky Toolbar */}
        <header className="h-16 border-b border-white/5 flex items-center justify-between px-8 bg-slate-950/60 backdrop-blur-xl z-30 sticky top-0">
          <div className="flex items-center gap-8">
            <button 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 rounded-lg hover:bg-white/5 text-slate-400 transition-colors"
            >
              <LayoutDashboard className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2 bg-white/5 p-1 rounded-xl border border-white/5">
              <button 
                onClick={() => setActiveTab('editor')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-widest transition-all ${activeTab === 'editor' ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20' : 'text-slate-500 hover:text-slate-300'}`}
              >
                <Code2 className="w-3.5 h-3.5" /> Source
              </button>
              <button 
                onClick={() => setActiveTab('explanation')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-widest transition-all ${activeTab === 'explanation' ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/20' : 'text-slate-500 hover:text-slate-300'}`}
              >
                <MessageSquare className="w-3.5 h-3.5" /> Documentation
              </button>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 mr-4 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
               <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
               <span className="text-[10px] font-black text-emerald-400 uppercase">Live Connection</span>
            </div>
            <button 
              onClick={() => handleAction('run')}
              disabled={isProcessing || !generatedCode}
              className="btn-primary px-6"
            >
              <Play className="w-4 h-4 fill-current" />
              Run Implementation
            </button>
          </div>
        </header>

        <div className="flex-1 flex overflow-hidden">
          {/* Main Stage: Editor or Explanation */}
          <div className="flex-1 flex flex-col border-r border-white/5 relative">
            <div className="flex-1 relative overflow-hidden">
              {activeTab === 'editor' ? (
                <div className="h-full animate-fade-in">
                  {generatedCode ? (
                    <div className="h-full p-6 pb-20">
                      <div className="h-full editor-container ring-1 ring-white/10 ring-inset">
                        <CodeEditor
                          code={generatedCode}
                          language={selectedLanguage}
                          onChange={setGeneratedCode}
                          height="100%"
                        />
                      </div>
                    </div>
                  ) : (
                    <div className="h-full flex flex-col items-center justify-center opacity-40">
                       <div className="p-8 rounded-3xl bg-white/5 border border-white/5 mb-6">
                         <Terminal className="w-16 h-16 text-blue-500" />
                       </div>
                       <h2 className="text-2xl font-bold mb-2">Workspace Empty</h2>
                       <p className="text-sm font-medium text-slate-500">Provide a prompt below to generate autonomous code.</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="h-full p-12 overflow-y-auto animate-fade-in bg-slate-900/20">
                  <div className="max-w-4xl mx-auto">
                    <h2 className="text-4xl font-bold mb-2 flex items-center gap-4">
                      <MessageSquare className="w-10 h-10 text-purple-400" />
                      Code Analysis
                    </h2>
                    <p className="text-slate-500 font-medium mb-12 uppercase tracking-[0.3em] text-xs">Generated by Explanation Agent</p>
                    
                    <div className="text-slate-200 leading-relaxed whitespace-pre-wrap font-mono text-sm bg-slate-800/40 p-10 rounded-[2rem] border border-white/5 shadow-2xl backdrop-blur-md">
                      {explanation || "Detailed analysis will appear here after generation."}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Bottom Panel: Console */}
            <div className="h-72 border-t border-white/5 bg-slate-950/40 backdrop-blur-2xl flex flex-col relative z-20">
              <div className="h-12 px-8 border-b border-white/5 flex items-center justify-between bg-white/5">
                <div className="flex items-center gap-3">
                  <Terminal className="w-4 h-4 text-blue-400" />
                  <span className="text-[11px] font-black uppercase tracking-[0.2em] text-slate-400">System Output & Console</span>
                </div>
                <button 
                  onClick={() => setOutput('')}
                  className="p-1.5 rounded-lg hover:bg-white/5 text-slate-500 hover:text-white transition-all"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
              <div className="flex-1 p-8 overflow-y-auto font-mono text-sm scrollbar-hide bg-black/20">
                <OutputConsole output={output} />
              </div>
            </div>

            {/* Floating Prompt Input */}
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 w-full max-w-3xl px-8 z-40">
              <div className="p-2.5 rounded-[2rem] bg-slate-900/80 backdrop-blur-3xl border border-white/10 shadow-[0_32px_64px_-12px_rgba(0,0,0,0.8)] ring-1 ring-white/5 flex items-center gap-4 group transition-all hover:border-blue-500/30">
                <div className="flex-1 relative pl-6">
                  <input 
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleAction('generate')}
                    placeholder="E.g. Create a high-performance factorial calculator with caching..."
                    className="w-full bg-transparent border-none focus:ring-0 text-base py-4 placeholder-slate-600 font-medium text-white"
                  />
                  <div className="absolute right-0 top-1/2 -translate-y-1/2 flex items-center gap-3">
                    <span className="text-[10px] text-slate-600 font-black border border-white/10 px-2 py-1 rounded-lg bg-white/5">ENTER</span>
                  </div>
                </div>
                <button 
                  onClick={() => handleAction('generate')}
                  disabled={isProcessing || !prompt.trim()}
                  className="bg-blue-600 hover:bg-blue-500 disabled:opacity-30 text-white w-14 h-14 rounded-[1.5rem] transition-all flex items-center justify-center shadow-lg shadow-blue-600/30 active:scale-90"
                >
                  {isProcessing ? (
                    <Loader2 className="w-6 h-6 animate-spin" />
                  ) : (
                    <ChevronRight className="w-7 h-7" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Right Panel: Agent Activity Workspace */}
          <div className="w-96 flex flex-col bg-slate-950/40 backdrop-blur-sm">
            <div className="p-8 border-b border-white/5">
              <div className="flex items-center gap-3 mb-1">
                <Activity className="w-5 h-5 text-blue-500 animate-pulse" />
                <h3 className="text-sm font-black uppercase tracking-[0.2em] text-white">Agent Workflow</h3>
              </div>
              <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Real-time Multi-Agent Activity</p>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-hide">
              {agentTasks.length > 0 ? (
                agentTasks.map((task, idx) => (
                  <div key={idx} className="animate-slide-up" style={{ animationDelay: `${idx * 150}ms` }}>
                    <AgentStatus task={task} />
                  </div>
                ))
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-slate-700 opacity-30 space-y-6">
                  <div className="p-8 rounded-[2.5rem] bg-white/5 border-2 border-dashed border-white/10">
                    <Bot className="w-12 h-12" />
                  </div>
                  <p className="text-xs font-black uppercase tracking-[0.3em] text-center">Waiting for Task<br/>Initialization</p>
                </div>
              )}
            </div>

            {/* Live Status Ticker */}
            <div className="h-64 border-t border-white/5 bg-black/40 p-8 flex flex-col relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-blue-500/30 to-transparent" />
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6 flex items-center justify-between">
                  <span>System Telemetry</span>
                  {isProcessing && <div className="flex gap-1.5">
                    <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" />
                    <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce [animation-delay:0.2s]" />
                    <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce [animation-delay:0.4s]" />
                  </div>}
                </p>
                <div className="flex-1 overflow-hidden relative">
                   <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent z-10 pointer-events-none" />
                   <LiveConsole messages={consoleMessages} />
                </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
