import React, { useState } from 'react';
import { Database, Table as TableIcon, ChevronRight, ChevronDown, Eye, Key, ExternalLink } from 'lucide-react';
import { SyntheticDatabase, TableDefinition } from '../../types';

interface SchemaExplorerProps {
  database: SyntheticDatabase;
  onPreviewTable: (table: TableDefinition) => void;
}

export const SchemaExplorer: React.FC<SchemaExplorerProps> = ({
  database,
  onPreviewTable,
}) => {
  const [expandedTables, setExpandedTables] = useState<Record<string, boolean>>({
    customers: true,
    orders: true,
  });

  const toggleTable = (tableName: string) => {
    setExpandedTables((prev) => ({
      ...prev,
      [tableName]: !prev[tableName],
    }));
  };

  return (
    <div className="flex flex-col h-full bg-dark-900 border-r border-dark-800 text-xs">
      
      {/* Schema Header */}
      <div className="p-3 border-b border-dark-800 bg-dark-950 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-brand-400" />
          <span className="font-semibold text-white font-mono tracking-tight">{database.name}</span>
        </div>
        <span className="text-[10px] px-1.5 py-0.5 rounded bg-dark-800 text-dark-400 font-mono">
          {database.tables.length} tables
        </span>
      </div>

      <div className="p-2 text-[11px] text-dark-400 bg-dark-950/40 border-b border-dark-800/60">
        Click a table to inspect columns or click the eye icon to preview sample records.
      </div>

      {/* Tables Accordion List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {database.tables.map((table) => {
          const isExpanded = !!expandedTables[table.name];
          return (
            <div
              key={table.name}
              className="border border-dark-800/80 rounded-lg overflow-hidden bg-dark-950/50"
            >
              {/* Table Bar */}
              <div className="flex items-center justify-between p-2 hover:bg-dark-800/50 transition-colors">
                <button
                  onClick={() => toggleTable(table.name)}
                  className="flex items-center gap-2 text-left flex-1 font-mono font-medium text-dark-200 hover:text-white"
                >
                  {isExpanded ? (
                    <ChevronDown className="w-3.5 h-3.5 text-dark-400" />
                  ) : (
                    <ChevronRight className="w-3.5 h-3.5 text-dark-400" />
                  )}
                  <TableIcon className="w-3.5 h-3.5 text-brand-400" />
                  <span>{table.name}</span>
                  <span className="text-[10px] text-dark-500 font-sans">
                    ({table.columns.length})
                  </span>
                </button>

                <button
                  onClick={() => onPreviewTable(table)}
                  title={`Preview sample data for ${table.name}`}
                  className="p-1 rounded text-dark-400 hover:text-brand-300 hover:bg-dark-800 transition-colors"
                >
                  <Eye className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Columns Details */}
              {isExpanded && (
                <div className="px-3 pb-2 pt-1 border-t border-dark-800/60 bg-dark-950/80 space-y-1.5">
                  {table.columns.map((col) => (
                    <div
                      key={col.name}
                      className="flex items-center justify-between text-[11px] font-mono py-0.5 text-dark-300"
                    >
                      <div className="flex items-center gap-1.5 truncate">
                        {col.isPrimaryKey ? (
                          <span title="Primary Key" className="text-amber-400">
                            <Key className="w-2.5 h-2.5" />
                          </span>
                        ) : col.isForeignKey ? (
                          <span title={`Foreign Key: ${col.references}`} className="text-blue-400">
                            <ExternalLink className="w-2.5 h-2.5" />
                          </span>
                        ) : (
                          <span className="w-2.5 h-2.5 rounded-full bg-dark-700/60 inline-block" />
                        )}
                        <span className="truncate hover:text-white">{col.name}</span>
                      </div>
                      <span className="text-[10px] text-dark-400 font-mono ml-2">
                        {col.type}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

