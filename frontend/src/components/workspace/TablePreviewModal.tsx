import React from 'react';
import { X, Table as TableIcon, Hash, Type, Key, ExternalLink } from 'lucide-react';
import { TableDefinition } from '../../types';

interface TablePreviewModalProps {
  table: TableDefinition | null;
  databaseName: string;
  onClose: () => void;
}

export const TablePreviewModal: React.FC<TablePreviewModalProps> = ({
  table,
  databaseName,
  onClose,
}) => {
  if (!table) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-4xl max-h-[85vh] bg-dark-900 border border-dark-700 rounded-xl shadow-2xl flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-dark-800 bg-dark-950">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-brand-500/10 text-brand-400 border border-brand-500/20">
              <TableIcon className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-dark-400">{databaseName} /</span>
                <h3 className="text-base font-bold text-white font-mono">{table.name}</h3>
                <span className="text-xs px-2 py-0.5 rounded bg-dark-800 text-dark-300 font-mono">
                  {table.rowCount} rows
                </span>
              </div>
              <p className="text-xs text-dark-400 mt-0.5">{table.description}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-dark-400 hover:text-white hover:bg-dark-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          
          {/* Columns & Schema Breakdown */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-dark-300 mb-3 flex items-center gap-1.5">
              <Hash className="w-3.5 h-3.5 text-brand-400" />
              Column Definitions & Constraints
            </h4>
            <div className="border border-dark-800 rounded-lg overflow-hidden bg-dark-950">
              <table className="w-full text-left text-xs">
                <thead className="bg-dark-900 text-dark-400 font-mono uppercase text-[10px] border-b border-dark-800">
                  <tr>
                    <th className="py-2.5 px-3">Column Name</th>
                    <th className="py-2.5 px-3">Data Type</th>
                    <th className="py-2.5 px-3">Keys / Constraints</th>
                    <th className="py-2.5 px-3">Nullable</th>
                    <th className="py-2.5 px-3">Description</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dark-800 font-mono">
                  {table.columns.map((col) => (
                    <tr key={col.name} className="hover:bg-dark-900/50 transition-colors">
                      <td className="py-2.5 px-3 font-semibold text-brand-300">{col.name}</td>
                      <td className="py-2.5 px-3 text-cyan-400">{col.type}</td>
                      <td className="py-2.5 px-3">
                        {col.isPrimaryKey && (
                          <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 text-[10px] border border-amber-500/20">
                            <Key className="w-2.5 h-2.5" /> PK
                          </span>
                        )}
                        {col.isForeignKey && (
                          <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 text-[10px] border border-blue-500/20 ml-1">
                            <ExternalLink className="w-2.5 h-2.5" /> FK ({col.references})
                          </span>
                        )}
                        {!col.isPrimaryKey && !col.isForeignKey && <span className="text-dark-500">—</span>}
                      </td>
                      <td className="py-2.5 px-3 text-dark-400">
                        {col.nullable ? 'YES' : 'NO'}
                      </td>
                      <td className="py-2.5 px-3 text-dark-300 font-sans text-xs">
                        {col.description || '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Sample Data Records */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-dark-300 mb-3 flex items-center gap-1.5">
              <Type className="w-3.5 h-3.5 text-brand-400" />
              Sample Records Preview ({table.sampleData.length} records)
            </h4>
            <div className="border border-dark-800 rounded-lg overflow-x-auto bg-dark-950">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-dark-900 text-dark-400 uppercase text-[10px] border-b border-dark-800">
                  <tr>
                    {table.columns.map((col) => (
                      <th key={col.name} className="py-2.5 px-3 whitespace-nowrap">
                        {col.name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-dark-800">
                  {table.sampleData.map((row, idx) => (
                    <tr key={idx} className="hover:bg-dark-900/40">
                      {table.columns.map((col) => (
                        <td key={col.name} className="py-2.5 px-3 text-dark-200 whitespace-nowrap">
                          {row[col.name] !== undefined && row[col.name] !== null ? (
                            String(row[col.name])
                          ) : (
                            <span className="text-dark-500 italic">NULL</span>
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-dark-800 bg-dark-950 flex items-center justify-between text-xs text-dark-400">
          <span>Inspect keys carefully before writing your JOIN predicates.</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-dark-800 hover:bg-dark-700 text-white font-medium transition-colors"
          >
            Close Preview
          </button>
        </div>

      </div>
    </div>
  );
};

