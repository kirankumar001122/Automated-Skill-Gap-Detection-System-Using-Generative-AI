'use client'

import { useEffect, useRef } from 'react'

interface Message {
  type: string
  message: string
}

export default function LiveConsole({ messages }: { messages: Message[] }) {
  const endRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const getStatusStyle = (type: string) => {
    switch (type.toLowerCase()) {
      case 'success': return { color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' }
      case 'error': return { color: 'text-rose-400', bg: 'bg-rose-500/10', border: 'border-rose-500/20' }
      case 'warning': return { color: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/20' }
      case 'info': return { color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/20' }
      default: return { color: 'text-slate-400', bg: 'bg-white/5', border: 'border-white/5' }
    }
  }

  return (
    <div className="flex-1 font-mono text-[10px] space-y-2.5 overflow-y-auto scrollbar-hide pr-2">
      {messages.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center opacity-10 gap-2">
          <div className="w-8 h-8 rounded-full border border-white border-t-transparent animate-spin" />
          <span className="font-black uppercase tracking-[0.3em]">Telemetry Link Offline</span>
        </div>
      ) : (
        <>
          {messages.map((msg, idx) => {
            const style = getStatusStyle(msg.type);
            return (
              <div 
                key={idx} 
                className={`flex flex-col gap-1 p-2 rounded-lg border transition-all animate-slide-up ${style.bg} ${style.border}`}
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <div className="flex items-center justify-between opacity-50">
                   <span className="font-bold text-[8px] uppercase tracking-widest text-slate-500">
                     Internal Log // {new Date().toLocaleTimeString([], { hour12: false, fractionalSecondDigits: 1 })}
                   </span>
                   <div className={`w-1 h-1 rounded-full ${style.color} shadow-[0_0_5px_currentColor]`} />
                </div>
                <div className="flex gap-2 items-start">
                  <span className={`font-black shrink-0 ${style.color} mt-0.5`}>›</span>
                  <span className={`${style.color} leading-tight font-medium`}>{msg.message}</span>
                </div>
              </div>
            )
          })}
          <div ref={endRef} />
        </>
      )}
    </div>
  )
}
