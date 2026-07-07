'use client'

import { useState, useEffect } from 'react'
import { CheckCircle2, XCircle, Loader2, Clock, Bot, Code2, Bug, Zap, Info, ClipboardList, Activity } from 'lucide-react'

interface AgentTask {
  agent_type: string
  status: string
  task_description?: string
  execution_time?: number
  error_message?: string
}

interface AgentStatusProps {
  task: AgentTask
}

export default function AgentStatus({ task }: AgentStatusProps) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    if (task.status === 'in_progress') {
      setProgress(5)
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 95) return prev;
          return prev + Math.floor(Math.random() * 5) + 2;
        });
      }, 500);
      return () => clearInterval(interval);
    } else if (task.status === 'completed') {
      setProgress(100);
    } else if (task.status === 'failed') {
      setProgress(task.status === 'failed' ? progress : 100);
    }
  }, [task.status])

  const getAgentInfo = (type: string) => {
    switch (type.toLowerCase()) {
      case 'planner':
        return { name: 'Software Architect', icon: <ClipboardList className="w-4 h-4" />, color: 'text-slate-400', glow: 'shadow-slate-500/20', bg: 'bg-slate-500/10' }
      case 'code_generator':
        return { name: 'Lead Developer', icon: <Code2 className="w-4 h-4" />, color: 'text-blue-400', glow: 'shadow-blue-500/20', bg: 'bg-blue-500/10' }
      case 'debug':
        return { name: 'Debug Engineer', icon: <Bug className="w-4 h-4" />, color: 'text-orange-400', glow: 'shadow-orange-500/20', bg: 'bg-orange-500/10' }
      case 'test':
        return { name: 'QA Specialist', icon: <CheckCircle2 className="w-4 h-4" />, color: 'text-emerald-400', glow: 'shadow-emerald-500/20', bg: 'bg-emerald-500/10' }
      case 'optimization':
        return { name: 'Perf Expert', icon: <Zap className="w-4 h-4" />, color: 'text-purple-400', glow: 'shadow-purple-500/20', bg: 'bg-purple-500/10' }
      case 'explanation':
        return { name: 'Tech Writer', icon: <Info className="w-4 h-4" />, color: 'text-cyan-400', glow: 'shadow-cyan-500/20', bg: 'bg-cyan-500/10' }
      default:
        return { name: 'Autonomous Agent', icon: <Bot className="w-4 h-4" />, color: 'text-slate-400', glow: 'shadow-slate-500/20', bg: 'bg-slate-500/10' }
    }
  }

  const info = getAgentInfo(task.agent_type)
  const isCompleted = task.status === 'completed'
  const isFailed = task.status === 'failed'
  const isInProgress = task.status === 'in_progress'

  return (
    <div className={`p-4 rounded-3xl border transition-all duration-500 group relative overflow-hidden ${
      isInProgress ? 'bg-slate-900 border-blue-500/30 shadow-[0_0_20px_rgba(59,130,246,0.1)]' :
      isCompleted ? 'bg-slate-900/40 border-emerald-500/20 shadow-none' :
      isFailed ? 'bg-rose-950/20 border-rose-500/30' :
      'bg-slate-900/20 border-white/5 opacity-40'
    }`}>
      {/* Background Pulse Effect */}
      {isInProgress && (
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-transparent animate-pulse" />
      )}
      
      {/* Progress Bar */}
      {(isInProgress || isCompleted || isFailed) && progress > 0 && (
        <div className="absolute bottom-0 left-0 h-1 bg-white/5 w-full">
           <div 
             className={`h-full ${isCompleted ? 'bg-emerald-500' : isFailed ? 'bg-rose-500' : 'bg-blue-500'} transition-all duration-500 ease-out`}
             style={{ width: `${progress}%` }}
           />
        </div>
      )}

      <div className="flex items-start justify-between relative z-10 mb-3">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${info.bg} ${info.color} shadow-lg ring-1 ring-white/10`}>
            {info.icon}
          </div>
          <div>
            <p className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 leading-none mb-1">{info.name}</p>
            <h4 className="text-xs font-bold text-white tracking-tight">
               {task.agent_type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} Agent
            </h4>
          </div>
        </div>

        <div className="flex flex-col items-end">
           {isInProgress ? (
             <div className="flex items-center gap-2 px-2 py-1 rounded-full bg-blue-500/10 border border-blue-500/20">
                <span className="text-[9px] font-black text-blue-400 uppercase tracking-tighter">Active</span>
                <Loader2 className="w-2.5 h-2.5 animate-spin text-blue-400" />
             </div>
           ) : isCompleted ? (
             <div className="w-5 h-5 rounded-full bg-emerald-500/20 flex items-center justify-center border border-emerald-500/40">
                <CheckCircle2 className="w-3 h-3 text-emerald-500" />
             </div>
           ) : isFailed ? (
             <div className="w-5 h-5 rounded-full bg-rose-500/20 flex items-center justify-center border border-rose-500/40">
                <XCircle className="w-3 h-3 text-rose-500" />
             </div>
           ) : (
             <Clock className="w-3.5 h-3.5 text-slate-700" />
           )}
        </div>
      </div>
      
      <div className="relative z-10 pl-1">
        <p className={`text-[11px] leading-relaxed mb-4 ${isInProgress ? 'text-slate-200' : 'text-slate-400'} font-medium`}>
          {task.task_description || 'Initializing phase...'}
        </p>
        
        <div className="flex items-center justify-between pt-3 border-t border-white/5 pb-1">
          <div className="flex items-center gap-2">
            <Activity className={`w-3 h-3 ${isInProgress ? 'text-blue-500 animate-pulse' : isCompleted ? 'text-emerald-500' : 'text-slate-700'}`} />
            <span className={`text-[9px] font-black uppercase tracking-widest ${isInProgress ? 'text-blue-500' : isCompleted ? 'text-emerald-500' : 'text-slate-600'}`}>
               {task.status.replace('_', ' ')}
               {(isInProgress || isCompleted) && ` - ${progress}%`}
            </span>
          </div>
          {task.execution_time && (
            <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-white/5 border border-white/5">
               <Clock className="w-2.5 h-2.5 text-slate-500" />
               <span className="text-[9px] font-bold font-mono text-slate-500">
                 {(task.execution_time * 1000).toFixed(0)}ms
               </span>
            </div>
          )}
        </div>
      </div>

      {isFailed && task.error_message && (
        <div className="mt-3 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 relative z-10 mb-2">
          <div className="flex items-center gap-2 mb-1.5">
             <XCircle className="w-3 h-3 text-rose-400" />
             <span className="text-[9px] font-black text-rose-400 uppercase tracking-widest">Error Trace</span>
          </div>
          <p className="text-[10px] text-rose-300/80 font-mono leading-relaxed break-words">
            {task.error_message}
          </p>
        </div>
      )}
    </div>
  )
}
