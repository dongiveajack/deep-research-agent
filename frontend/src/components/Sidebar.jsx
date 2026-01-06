import React from 'react';
import { Plus, MessageSquare, Trash2, Moon, Sun, LogOut } from 'lucide-react';
import { client } from '../utils/langgraph';

export function Sidebar({
    threads,
    currentThreadId,
    onSelectThread,
    onCreateThread,
    onDeleteThread,
    theme,
    onToggleTheme,
    onLogout
}) {
    return (
        <div className="w-64 bg-gray-50 dark:bg-neutral-900 border-r border-gray-200 dark:border-neutral-800 h-screen flex flex-col transition-colors duration-200">
            <div className="p-4">
                <button
                    onClick={onCreateThread}
                    className="w-full flex items-center justify-center gap-2 bg-black dark:bg-neutral-700 text-white dark:text-white px-4 py-2 rounded-lg hover:bg-gray-800 dark:hover:bg-neutral-600 transition-colors"
                >
                    <Plus size={18} />
                    New Chat
                </button>
            </div>

            <div className="flex-1 overflow-y-auto">
                <div className="px-3 pb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    Recent Chats
                </div>
                <div className="space-y-1 px-2">
                    {threads.map((thread) => (
                        <div
                            key={thread.thread_id}
                            className={`group flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-colors text-sm ${currentThreadId === thread.thread_id
                                ? 'bg-white dark:bg-neutral-800 shadow-sm border border-gray-200 dark:border-neutral-700 text-gray-900 dark:text-neutral-100'
                                : 'text-gray-600 dark:text-neutral-400 hover:bg-gray-100 dark:hover:bg-neutral-800'
                                }`}
                            onClick={() => onSelectThread(thread.thread_id)}
                        >
                            <MessageSquare size={16} className="shrink-0" />
                            <div className="flex-1 truncate">
                                {thread.values?.topic || new Date(thread.created_at).toLocaleString()}
                            </div>
                            {onDeleteThread && (
                                <button
                                    onClick={(e) => { e.stopPropagation(); onDeleteThread(thread.thread_id); }}
                                    className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-200 rounded"
                                >
                                    <Trash2 size={14} />
                                </button>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            <div className="p-4 border-t border-gray-200 dark:border-neutral-800 flex items-center justify-between">
                <button
                    onClick={onLogout}
                    className="flex items-center gap-2 text-xs text-gray-500 hover:text-red-600 dark:text-neutral-400 dark:hover:text-red-400 transition-colors"
                    title="Logout"
                >
                    <LogOut size={14} />
                    <span>Exit</span>
                </button>

                <button
                    onClick={onToggleTheme}
                    className="p-1.5 text-gray-500 hover:text-gray-900 dark:text-neutral-400 dark:hover:text-white hover:bg-gray-200 dark:hover:bg-neutral-800 rounded-md transition-colors"
                >
                    {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
                </button>
            </div>
        </div>
    );
}
