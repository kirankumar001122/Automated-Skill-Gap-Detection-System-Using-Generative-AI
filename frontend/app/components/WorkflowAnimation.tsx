'use client'

const AGENTS = [
  { name: 'Planner', icon: '📋', color: 'from-blue-500 to-blue-600' },
  { name: 'Generator', icon: '⚙️', color: 'from-purple-500 to-purple-600' },
  { name: 'Debug', icon: '🔍', color: 'from-orange-500 to-orange-600' },
  { name: 'Test', icon: '✓', color: 'from-green-500 to-green-600' },
  { name: 'Optimize', icon: '⚡', color: 'from-yellow-500 to-yellow-600' },
  { name: 'Explain', icon: '📝', color: 'from-pink-500 to-pink-600' }
]

export default function WorkflowAnimation({ isActive }: { isActive: boolean }) {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center gap-4">
      <div className="space-y-3 w-full">
        {AGENTS.map((agent, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-lg border transition-all duration-500 ${
              isActive
                ? `bg-gradient-to-r ${agent.color} border-transparent shadow-lg animate-pulse`
                : 'bg-slate-700/30 border-slate-600/50'
            }`}
          >
            <div className="flex items-center gap-2">
              <span className="text-xl">{agent.icon}</span>
              <span className="text-sm font-semibold flex-1">{agent.name}</span>
              {isActive && (
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {isActive && (
        <div className="mt-4 text-center">
          <div className="inline-block">
            <svg className="w-8 h-8 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <p className="text-xs text-slate-400 mt-2">Processing agents...</p>
        </div>
      )}
    </div>
  )
}
