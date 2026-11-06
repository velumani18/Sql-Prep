import React, { useRef } from 'react';
import Editor, { OnMount } from '@monaco-editor/react';

interface MonacoSQLEditorProps {
  value: string;
  onChange: (value: string) => void;
  onRunQuery: () => void;
  readOnly?: boolean;
}

export const MonacoSQLEditor: React.FC<MonacoSQLEditorProps> = ({
  value,
  onChange,
  onRunQuery,
  readOnly = false,
}) => {
  const editorRef = useRef<any>(null);

  const handleEditorDidMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;

    // Define custom dark theme matching the app aesthetic
    monaco.editor.defineTheme('sqlforge-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'keyword', foreground: '34d399', fontStyle: 'bold' },
        { token: 'string', foreground: 'fcd34d' },
        { token: 'number', foreground: '60a5fa' },
        { token: 'comment', foreground: '64748b', fontStyle: 'italic' },
        { token: 'operator', foreground: '38bdf8' },
        { token: 'identifier', foreground: 'e2e8f0' },
      ],
      colors: {
        'editor.background': '#090d16',
        'editor.foreground': '#f1f5f9',
        'editorLineNumber.foreground': '#334155',
        'editorLineNumber.activeForeground': '#34d399',
        'editor.lineHighlightBackground': '#11182740',
        'editor.selectionBackground': '#10b98130',
        'editorCursor.foreground': '#34d399',
      },
    });

    monaco.editor.setTheme('sqlforge-dark');

    // Add Ctrl+Enter / Cmd+Enter execution shortcut
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
      onRunQuery();
    });
  };

  return (
    <div className="w-full h-full relative overflow-hidden bg-dark-950">
      <Editor
        height="100%"
        defaultLanguage="sql"
        value={value}
        onChange={(val) => onChange(val || '')}
        onMount={handleEditorDidMount}
        theme="sqlforge-dark"
        options={{
          fontSize: 13.5,
          fontFamily: "'JetBrains Mono', 'Fira Code', Menlo, Monaco, 'Courier New', monospace",
          fontLigatures: true,
          lineNumbers: 'on',
          lineNumbersMinChars: 3,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          insertSpaces: true,
          wordWrap: 'on',
          readOnly,
          suggestOnTriggerCharacters: true,
          quickSuggestions: true,
          formatOnPaste: true,
          cursorBlinking: 'smooth',
          cursorSmoothCaretAnimation: 'on',
          overviewRulerBorder: false,
          hideCursorInOverviewRuler: true,
          padding: { top: 12, bottom: 12 },
        }}
      />
    </div>
  );
};

