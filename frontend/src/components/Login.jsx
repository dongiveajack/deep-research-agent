import React, { useState } from 'react';
import { ArrowRight, Lock, User, Sparkles, Globe, ShieldCheck } from 'lucide-react';

export function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!username || !password) return;

        setIsLoading(true);
        // Simulate network delay for a realistic feel
        setTimeout(() => {
            onLogin(username);
            setIsLoading(false);
        }, 800);
    };

    return (
        <div className="fixed inset-0 flex bg-white dark:bg-neutral-950 transition-colors duration-500">

            {/* Left Panel - Branding & Value Prop */}
            <div className="hidden lg:flex lg:w-1/2 bg-black dark:bg-neutral-900 relative overflow-hidden flex-col justify-between p-16 text-white">
                {/* Background Pattern */}
                <div className="absolute inset-0 opacity-20">
                    <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-blue-600 rounded-full blur-[120px] -translate-y-1/2 translate-x-1/2" />
                    <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-purple-600 rounded-full blur-[120px] translate-y-1/2 -translate-x-1/2" />
                </div>

                {/* Header */}
                <div className="relative z-10 flex items-center gap-3">
                    <div className="w-10 h-10 bg-white/10 backdrop-blur-md rounded-xl flex items-center justify-center border border-white/10">
                        <Sparkles className="w-5 h-5 text-blue-400" />
                    </div>
                    <span className="text-xl font-bold tracking-tight">Research Agent</span>
                </div>

                {/* Hero Content */}
                <div className="relative z-10 space-y-8 max-w-lg">
                    <h1 className="text-5xl font-bold leading-tight">
                        Autonomous <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
                            Deep Research.
                        </span>
                    </h1>
                    <p className="text-lg text-gray-400 leading-relaxed">
                        An intelligent agent that plans, researches, and synthesizes. Guide the workflow with human-in-the-loop approval and let the agent handle the complexity.
                    </p>

                    {/* Feature Pills */}
                    <div className="flex gap-4 pt-4">
                        <div className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm font-medium">
                            <Globe className="w-4 h-4 text-blue-400" />
                            <span>Web Scale Search</span>
                        </div>
                        <div className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm font-medium">
                            <ShieldCheck className="w-4 h-4 text-purple-400" />
                            <span>Human-in-the-loop</span>
                        </div>
                    </div>
                </div>

                {/* Footer */}
                <div className="relative z-10 text-sm text-gray-500">
                    © 2024 LangGraph Research. All rights reserved.
                </div>
            </div>

            {/* Right Panel - Login Form */}
            <div className="flex-1 flex flex-col items-center justify-center p-8 bg-gray-50 dark:bg-neutral-950">
                <div className="w-full max-w-md space-y-8">
                    <div className="text-center lg:text-left">
                        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Sign in to your account</h2>
                        <p className="mt-2 text-gray-600 dark:text-neutral-400">
                            Enter your credentials to access the workspace
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-neutral-300 mb-2">Username</label>
                                <div className="relative group">
                                    <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-black dark:group-focus-within:text-white transition-colors" />
                                    <input
                                        type="text"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                        className="w-full bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-xl pl-12 pr-4 py-4 outline-none focus:border-black dark:focus:border-white focus:ring-1 focus:ring-black dark:focus:ring-white transition-all dark:text-white"
                                        placeholder="Enter your username"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-neutral-300 mb-2">Password</label>
                                <div className="relative group">
                                    <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-black dark:group-focus-within:text-white transition-colors" />
                                    <input
                                        type="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="w-full bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-xl pl-12 pr-4 py-4 outline-none focus:border-black dark:focus:border-white focus:ring-1 focus:ring-black dark:focus:ring-white transition-all dark:text-white"
                                        placeholder="Enter your password"
                                    />
                                </div>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={!username || !password || isLoading}
                            className="w-full bg-black dark:bg-white text-white dark:text-black h-14 rounded-xl font-medium text-lg shadow-lg hover:shadow-xl hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
                        >
                            {isLoading ? (
                                <div className="w-6 h-6 border-2 border-white/30 dark:border-black/30 border-t-white dark:border-t-black rounded-full animate-spin" />
                            ) : (
                                <>
                                    Sign In <ArrowRight className="w-5 h-5" />
                                </>
                            )}
                        </button>
                    </form>

                    <p className="text-center text-sm text-gray-500">
                        Don't have an account? <span className="text-black dark:text-white font-medium cursor-not-allowed opacity-50">Contact Admin</span>
                    </p>
                </div>
            </div>
        </div>
    );
}
