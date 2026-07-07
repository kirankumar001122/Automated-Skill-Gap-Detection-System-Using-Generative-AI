'use client'

import { Send, Loader2 } from 'lucide-react'

interface PromptInputProps {
  prompt: string
  onPromptChange: (prompt: string) => void
  onGenerate: () => void
  isProcessing: boolean
  language: string
}

export default function PromptInput({
  prompt,
  onPromptChange,
  onGenerate,
  isProcessing,
  language
}: PromptInputProps) {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      onGenerate()
    }
  }

  return (
    <div className="flex flex-col h-full gap-3">
      <div className="flex-1 flex flex-col">
        <h3 className="text-sm font-semibold text-slate-300 mb-2">
          💡 Enter Your Prompt
        </h3>
        <textarea
          value={prompt}
          onChange={(e) => onPromptChange(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Describe the code you want to generate... (Ctrl+Enter to submit)"
          className="w-full flex-1 px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none resize-none text-sm"
          disabled={isProcessing}
        />
      </div>

      <button
        onClick={onGenerate}
        disabled={!prompt.trim() || isProcessing}
        className="w-full px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 text-white font-semibold rounded-lg transition-all flex items-center justify-center gap-2"
      >
        {isProcessing ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Processing...
          </>
        ) : (
          <>
            <Send className="w-4 h-4" />
            Generate Code
          </>
        )}
      </button>

      {/* Help Text */}
      <div className="text-xs text-gray-500 space-y-1">
        <p>• Be specific about requirements</p>
        <p>• Mention any libraries or frameworks</p>
        <p>• Include expected inputs/outputs</p>
        <p>• Press Ctrl+Enter to generate</p>
      </div>
    </div>
  )
}
