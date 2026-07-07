'use client'

import { useState } from 'react'
import Editor from '@monaco-editor/react'

interface CodeEditorProps {
  code: string
  onChange: (value: string) => void
  language: string
  height?: string
}

export default function CodeEditor({ 
  code, 
  onChange, 
  language, 
  height = '100%'
}: CodeEditorProps) {
  const [editor, setEditor] = useState<any>(null)

  const handleEditorDidMount = (editor: any, monaco: any) => {
    setEditor(editor)
    
    // Define custom theme
    monaco.editor.defineTheme('antigravity-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#0d1117',
        'editor.lineHighlightBackground': '#ffffff05',
        'editorLineNumber.foreground': '#4b5563',
        'editorLineNumber.activeForeground': '#3b82f6',
        'editor.selectionBackground': '#3b82f633',
        'editor.inactiveSelectionBackground': '#3b82f611',
        'editorCursor.foreground': '#3b82f6',
        'editorIndentGuide.background': '#ffffff08',
        'editorIndentGuide.activeBackground': '#ffffff15',
      }
    });

    monaco.editor.setTheme('antigravity-dark');

    // Configure editor options
    editor.updateOptions({
      fontSize: 15,
      lineHeight: 24,
      wordWrap: 'on',
      minimap: { enabled: true, scale: 0.7, side: 'right' },
      scrollBeyondLastLine: false,
      automaticLayout: true,
      tabSize: 2,
      insertSpaces: true,
      fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
      fontWeight: '400',
      letterSpacing: 0.5,
    })
  }

  const handleEditorChange = (value: string | undefined) => {
    onChange(value || '')
  }

  const getMonacoLanguage = (lang: string) => {
    const languageMap: { [key: string]: string } = {
      'python': 'python',
      'javascript': 'javascript',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c',
      'typescript': 'typescript',
      'html': 'html',
      'css': 'css',
      'json': 'json',
      'sql': 'sql'
    }
    return languageMap[lang.toLowerCase()] || 'plaintext'
  }

  return (
    <div className="w-full h-full flex flex-col bg-[#0d1117]">
      <div className="bg-[#161b22] px-6 py-3 border-b border-white/5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-rose-500/80 shadow-[0_0_8px_rgba(244,63,94,0.3)]" />
            <div className="w-3 h-3 rounded-full bg-amber-500/80 shadow-[0_0_8px_rgba(245,158,11,0.3)]" />
            <div className="w-3 h-3 rounded-full bg-emerald-500/80 shadow-[0_0_8px_rgba(16,185,129,0.3)]" />
          </div>
          <div className="h-4 w-px bg-white/10 mx-1" />
          <span className="text-[10px] font-black uppercase tracking-[0.25em] text-slate-500">
            {language.toUpperCase()} <span className="text-blue-500/60">Module</span>
          </span>
        </div>
        <div className="flex items-center gap-4">
           <span className="text-[10px] font-bold text-slate-600 uppercase tracking-widest">{code.split('\n').length} Lines</span>
           <div className="px-2 py-0.5 rounded bg-blue-500/10 border border-blue-500/20 text-[9px] font-black text-blue-500 uppercase tracking-tighter">
             Auto-Synced
           </div>
        </div>
      </div>
      <div className="flex-1">
        <Editor
          height="100%"
          language={getMonacoLanguage(language)}
          value={code}
          onChange={handleEditorChange}
          onMount={handleEditorDidMount}
          options={{
            selectOnLineNumbers: true,
            suggestOnTriggerCharacters: true,
            acceptSuggestionOnEnter: 'on',
            tabCompletion: 'on',
            wordBasedSuggestions: "currentDocument",
            parameterHints: { enabled: true },
            hover: { enabled: true },
            quickSuggestions: true,
            showFoldingControls: 'always',
            smoothScrolling: true,
            cursorBlinking: 'smooth',
            cursorSmoothCaretAnimation: 'on',
            renderLineHighlight: 'all',
            renderWhitespace: 'none',
            bracketPairColorization: { enabled: true },
            guides: { bracketPairs: true, indentation: true },
            lineNumbers: 'on',
            glyphMargin: false,
            folding: true,
            lineDecorationsWidth: 10,
            lineNumbersMinChars: 3,
            padding: { top: 20, bottom: 20 },
            scrollbar: {
              vertical: 'visible',
              horizontal: 'visible',
              useShadows: false,
              verticalScrollbarSize: 10,
              horizontalScrollbarSize: 10
            }
          }}
        />
      </div>
    </div>
  )
}
