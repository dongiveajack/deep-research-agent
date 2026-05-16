import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatInterface } from './components/ChatInterface';
import { client } from './utils/langgraph';
import { useTheme } from './hooks/useTheme';
import { Login } from './components/Login';

function App() {
  const { theme, toggleTheme } = useTheme();
  const [threads, setThreads] = useState([]);
  const [currentThreadId, setCurrentThreadId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Fetch threads on mount
  useEffect(() => {
    async function fetchThreads() {
      try {
        const result = await client.threads.search({ limit: 50 });
        setThreads(result);
        if (result.length > 0) {
          setCurrentThreadId(result[0].thread_id);
        }
      } catch (error) {
        console.error("Failed to fetch threads:", error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchThreads();
  }, []);

  const handleCreateThread = async () => {
    try {
      const thread = await client.threads.create();
      setThreads([thread, ...threads]);
      setCurrentThreadId(thread.thread_id);
    } catch (error) {
      console.error("Failed to create thread:", error);
    }
  };

  const handleDeleteThread = async (threadId) => {
    // Optimistic update
    setThreads(threads.filter(t => t.thread_id !== threadId));
    if (currentThreadId === threadId) {
      setCurrentThreadId(null);
    }
    try {
      await client.threads.delete(threadId);
    } catch (e) {
      console.error("Failed to delete thread", e);
      // Revert if needed, but for now simplistic
    }
  }

  if (!isAuthenticated) {
    return <Login onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <div className="flex h-screen w-full bg-white dark:bg-neutral-950 overflow-hidden transition-colors duration-200">
      <Sidebar
        threads={threads}
        currentThreadId={currentThreadId}
        onSelectThread={setCurrentThreadId}
        onCreateThread={handleCreateThread}
        onDeleteThread={handleDeleteThread}
        theme={theme}
        onToggleTheme={toggleTheme}
        onLogout={() => setIsAuthenticated(false)}
      />

      {currentThreadId ? (
        <ChatInterface key={currentThreadId} threadId={currentThreadId} />
      ) : (
        <div className="flex-1 flex items-center justify-center text-gray-400">
          Select or create a chat to begin
        </div>
      )}
    </div>
  );
}

export default App;
