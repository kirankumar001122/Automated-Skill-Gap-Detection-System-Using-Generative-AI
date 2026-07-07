'use client'

import { Terminal, ShieldCheck, AlertTriangle, ChevronRight } from 'lucide-react'

interface OutputConsoleProps {
  output: string
}

export default function OutputConsole({ output }: OutputConsoleProps) {
  if (!output) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-slate-800 font-mono gap-4 animate-pulse">
        <Terminal className="w-10 h-10 opacity-20" />
        <span className="text-xs font-black uppercase tracking-[0.4em] opacity-40">System Idle</span>
      </div>
    )
  }

  const isRunning = output === 'Running...'
  const isCompilationError = output.toLowerCase().includes('compilation error')
  const isRuntimeError = !isCompilationError && (output.toLowerCase().includes('error') || 
                  output.toLowerCase().includes('exception') || 
                  output.toLowerCase().includes('failed') ||
                  output.toLowerCase().includes('traceback'))
  const isError = isCompilationError || isRuntimeError

  const getStatusText = () => {
    if (isRunning) return 'Process Terminal - RUNNING'
    if (isCompilationError) return 'Process Terminal - COMPILATION ERROR'
    if (isRuntimeError) return 'Process Terminal - RUNTIME ERROR'
    return 'Process Terminal - SUCCESS'
  }
  
  const getStatusColor = () => {
    if (isRunning) return 'text-blue-500'
    if (isError) return 'text-rose-500'
    return 'text-emerald-500'
  }
  
  const getDotColor = () => {
    if (isRunning) return 'bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.6)] animate-pulse'
    if (isError) return 'bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.6)]'
    return 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)]'
  }

  return (
    <div className="h-full w-full font-mono text-sm leading-relaxed overflow-x-auto">
      <div className="flex items-center justify-between mb-6 border-b border-white/5 pb-4">
        <div className="flex items-center gap-3">
          <div className={`w-2 h-2 rounded-full ${getDotColor()}`} />
          <span className={`text-[10px] font-black uppercase tracking-[0.2em] ${getStatusColor()}`}>
            {getStatusText()}
          </span>
        </div>
        <div className="flex items-center gap-4 text-[9px] font-bold text-slate-600 uppercase tracking-tighter">
           <span className="flex items-center gap-1"><ShieldCheck className="w-3 h-3" /> Secure</span>
           <span className="flex items-center gap-1"><Terminal className="w-3 h-3" /> Local</span>
        </div>
      </div>
      
      <div className="space-y-4">
        <div className="flex gap-3">
           <ChevronRight className="w-4 h-4 text-slate-700 flex-shrink-0 mt-0.5" />
           <pre className={`whitespace-pre-wrap break-words font-medium ${isError ? 'text-rose-400' : 'text-slate-300'}`}>
             {output}
           </pre>
        </div>
        
        {isError && (
          <div className="mt-6 p-4 rounded-2xl bg-rose-500/5 border border-rose-500/10 flex gap-4 items-start">
             <AlertTriangle className="w-5 h-5 text-rose-500 flex-shrink-0" />
             <div>
                <h5 className="text-[10px] font-black uppercase tracking-widest text-rose-500 mb-1">Execution Failure detected</h5>
                <p className="text-[11px] text-rose-400/70 font-medium">The local runner encountered an error during code execution. Debug agent recommended.</p>
             </div>
          </div>
        )}
        
        <div className="flex items-center gap-1">
           <span className="text-blue-500 font-bold tracking-tighter">$</span>
           <div className="w-2 h-4 bg-blue-500/80 animate-[pulse_1s_infinite] shadow-[0_0_8px_rgba(59,130,246,0.6)] ml-1" />
        </div>
      </div>
    </div>
  )
}
