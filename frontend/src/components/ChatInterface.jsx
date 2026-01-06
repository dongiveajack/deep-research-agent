import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, RefreshCw, AlertCircle, Check, Play, Edit2, ArrowUp } from 'lucide-react';
import { client } from '../utils/langgraph';

function PlanReview({ interruptValue, onApprove, onReject }) {
    const [queries, setQueries] = useState(interruptValue['Research Websites'] || []);
    const [isEditing, setIsEditing] = useState(false);

    const handleApprove = () => {
        onApprove({
            start_research: 'Approved',
            generated_queries: queries
        });
    };

    return (
        <div className="bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-lg shadow-sm p-4 w-full max-w-2xl my-4">
            <div className="flex items-start gap-3">
                <div className="bg-blue-50 p-2 rounded-full text-blue-600 mt-1">
                    <AlertCircle size={20} />
                </div>
                <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-white">Review Research Plan</h3>
                    <p className="text-sm text-gray-600 dark:text-neutral-400 mt-1">
                        The agent has proposed the following research queries for topic: <span className="font-medium text-black dark:text-white">"{interruptValue.user_query}"</span>
                    </p>

                    <div className="mt-3 bg-gray-50 rounded-md p-3">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-xs font-semibold text-gray-500 uppercase">Proposed Queries</span>
                            <button
                                onClick={() => setIsEditing(!isEditing)}
                                className="text-xs flex items-center gap-1 text-gray-500 hover:text-black dark:text-neutral-400 dark:hover:text-white"
                            >
                                <Edit2 size={12} /> {isEditing ? 'Done' : 'Edit'}
                            </button>
                        </div>
                        {isEditing ? (
                            <textarea
                                className="w-full text-sm p-2 border rounded"
                                rows={5}
                                value={queries.join('\n')}
                                onChange={(e) => setQueries(e.target.value.split('\n'))}
                            />
                        ) : (
                            <ul className="list-disc list-inside text-sm space-y-1 text-gray-700">
                                {queries.map((q, i) => (
                                    <li key={i}>{q}</li>
                                ))}
                            </ul>
                        )}
                    </div>

                    <div className="flex gap-3 mt-4">
                        <button
                            onClick={handleApprove}
                            className="flex items-center gap-2 bg-black dark:bg-neutral-700 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-800 dark:hover:bg-neutral-600 transition-colors"
                        >
                            <Check size={16} /> Approve & Start
                        </button>
                        {/* 
            <button
              onClick={() => onReject()} // Not fully implemented in graph yet?
              className="px-4 py-2 text-sm text-gray-600 hover:text-red-600 transition-colors"
            >
              Reject
            </button>
            */}
                    </div>
                </div>
            </div>
        </div >
    );
}

export function ChatInterface({ threadId }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [loadingText, setLoadingText] = useState('Thinking...');
    const [interrupt, setInterrupt] = useState(null);
    const bottomRef = useRef(null);

    // Load history and check state
    useEffect(() => {
        if (!threadId) return;

        const fetchState = async () => {
            try {
                const state = await client.threads.getState(threadId);
                const msgs = [];
                if (state.values?.messages && state.values.messages.length > 0) {
                    state.values.messages.forEach(m => {
                        // Handle langchain message objects (they might be serialized or real objects)
                        const role = m.type === 'human' || m.role === 'user' ? 'human' : 'ai';
                        const content = m.content || m.text;
                        if (content) {
                            msgs.push({ type: role, content: content });
                        }
                    });
                    setMessages(msgs);
                }

                // Check for interrupts
                if (state.tasks && state.tasks.length > 0) {
                    const lastTask = state.tasks[0];
                    if (lastTask.interrupts && lastTask.interrupts.length > 0) {
                        setInterrupt(lastTask.interrupts[0].value);
                    } else {
                        setInterrupt(null);
                    }
                }
            } catch (e) {
                console.error("Error fetching state:", e);
            }
        };

        fetchState();
        setMessages([]); // Reset on thread change before load
        setInterrupt(null);
    }, [threadId]);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, interrupt, isLoading]);

    const streamRun = async (streamRequest, isResume = false) => {
        setIsLoading(true);
        setInterrupt(null);
        if (!isResume) {
            // Optimistic add user message with a marker for the current turn
            setMessages(prev => [...prev, { type: 'human', content: input, turnBoundary: true }]);
            setInput('');
        }
        setLoadingText('Thinking...');

        try {
            const stream = client.runs.stream(
                threadId,
                "agent",
                streamRequest
            );

            for await (const event of stream) {
                if (event.event === 'values') {
                    const values = event.data;

                    // Update loading text
                    if (values.next_node === 'research') {
                        setLoadingText('Researching...');
                    } else if (values.next_node === 'conversation') {
                        setLoadingText('Thinking...');
                    }

                    // Check if we have new messages
                    if (values.messages && values.messages.length > 0) {
                        setMessages(prev => {
                            const newMsgs = [];
                            values.messages.forEach(m => {
                                const role = m.type === 'human' || m.role === 'user' ? 'human' : 'ai';
                                const content = m.content || m.text;
                                if (content) {
                                    newMsgs.push({ type: role, content: content });
                                }
                            });
                            // Simple merge: mostly replacing with server state as it's the source of truth for 'values' mode
                            // But we might want to keep the local optimistic human message if it hasn't round-tripped yet? 
                            // Actually, 'values' usually gives the full state. If we trust it, we can just replace.
                            // BUT, visually we want to avoid flickering. 
                            // Let's stick to the previous pattern of updating the last AI message if we can identifying it from 'messages'

                            return newMsgs;
                        });
                    }
                }
            }

            // After stream, check if we stopped for interrupt
            const state = await client.threads.getState(threadId);
            if (state.tasks && state.tasks.length > 0 && state.tasks[0].interrupts?.length > 0) {
                setInterrupt(state.tasks[0].interrupts[0].value);
            } else {
                setInterrupt(null);
            }

        } catch (e) {
            console.error("Stream error:", e);
            setMessages(prev => [...prev, { type: 'error', content: "An error occurred." }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSend = () => {
        if (!input.trim()) return;
        setLoadingText('Thinking...');
        // Sending as a message to support multi-turn and supervisor logic
        streamRun({ input: { messages: [{ role: "user", content: input }] }, streamMode: "values" });
    };

    const handleInterruptResponse = (response) => {
        streamRun({ command: { resume: response }, streamMode: "values" }, true);
    };

    return (
        <div className="flex-1 h-screen relative flex flex-col bg-white dark:bg-neutral-950 transition-colors duration-200">
            {/* Header */}
            <div className="h-14 border-b border-gray-100 dark:border-neutral-800 flex items-center px-6 justify-between bg-white/80 dark:bg-neutral-950/80 backdrop-blur-md sticky top-0 z-10 transition-all">
                <h2 className="font-semibold text-gray-800 dark:text-neutral-200 flex items-center gap-2">
                    Research Agent
                </h2>
                <div className="text-xs font-mono text-gray-400">ID: {threadId.slice(0, 8)}...</div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-6 scroll-smooth">
                <div className="max-w-5xl mx-auto space-y-6">
                    {messages.length === 0 && !isLoading && !interrupt ? (
                        <div className="flex flex-col items-center justify-center h-full text-center text-gray-400 opacity-50 min-h-[400px]">
                            <div className="mb-2">Enter a topic to begin deep research.</div>
                        </div>
                    ) : (
                        messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`flex gap-3 ${msg.type === 'human' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`rounded-2xl px-5 py-3.5 shadow-sm text-sm leading-relaxed ${msg.type === 'human'
                                        ? 'bg-neutral-800 dark:bg-zinc-200 text-white dark:text-neutral-900 rounded-br-none max-w-[85%] sm:max-w-2xl'
                                        : 'bg-white dark:bg-neutral-900 border border-gray-100 dark:border-neutral-800 text-gray-800 dark:text-neutral-200 rounded-bl-none w-full'
                                        }`}
                                >
                                    {msg.type === 'error' ? (
                                        <span className="text-red-500">{msg.content}</span>
                                    ) : (
                                        <div className={`prose prose-sm max-w-none ${msg.type === 'human'
                                            ? 'prose-invert dark:prose-neutral' // Human: Dark bg (Light) -> Invert. Light bg (Dark) -> Normal.
                                            : 'dark:prose-invert' // AI: White bg (Light) -> Normal. Dark bg (Dark) -> Invert.
                                            }`}>
                                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))
                    )}

                    {interrupt && (
                        <div className="flex justify-start animate-in fade-in slide-in-from-bottom-2">
                            <PlanReview
                                interruptValue={interrupt}
                                onApprove={handleInterruptResponse}
                                onReject={() => console.log("Rejected")}
                            />
                        </div>
                    )}

                    {isLoading && !interrupt && (
                        <div className="flex justify-start">
                            <div className="bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-2xl px-4 py-3 flex items-center gap-3 shadow-sm">
                                <RefreshCw className="animate-spin text-gray-400" size={16} />
                                <span className="text-sm text-gray-500 dark:text-neutral-400">{loadingText}</span>
                            </div>
                        </div>
                    )}                    {/* Spacer for floating input - ensures scrollToView leaves space */}
                    <div ref={bottomRef} className="h-64 w-full block" />
                </div>
            </div>

            {/* Input */}
            <div className="absolute bottom-0 left-0 right-0 z-20 p-4 sm:p-6 pt-12 bg-gradient-to-t from-white via-white to-transparent dark:from-neutral-950 dark:via-neutral-950 dark:to-transparent">
                <div className="relative max-w-5xl mx-auto">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                        placeholder={interrupt ? "Approve the plan above to continue..." : "Enter a research topic..."}
                        disabled={!!interrupt || isLoading}
                        className="w-full bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-neutral-700 rounded-3xl px-5 py-5 pr-14 resize-none focus:outline-none focus:ring-2 focus:ring-black/5 dark:focus:ring-white/10 focus:border-gray-300 dark:focus:border-neutral-600 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed text-sm text-black dark:text-white placeholder:text-gray-500 dark:placeholder:text-neutral-400"
                        rows={1}
                        style={{ minHeight: '60px' }}
                    />
                    <button
                        onClick={handleSend}
                        disabled={!input.trim() || isLoading || !!interrupt}
                        className="absolute right-3 top-[46%] -translate-y-1/2 h-10 w-10 flex items-center justify-center p-0 bg-black dark:bg-neutral-700 text-white dark:text-white rounded-full hover:bg-gray-800 dark:hover:bg-neutral-600 disabled:opacity-30 disabled:hover:bg-black transition-all shadow-md hover:shadow-lg hover:scale-105 active:scale-95 duration-200"
                    >
                        {isLoading ? <RefreshCw className="animate-spin" size={20} /> : <ArrowUp size={20} strokeWidth={2.5} />}
                    </button>
                </div>
            </div>
        </div>
    );
}
