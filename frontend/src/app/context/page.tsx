"use client";
import { mockContextEntries } from "@/mock";
import { useState } from "react";

const sourceTypes = ["WhatsApp", "Email", "Note"];

export default function ContextPage() {
  const [entries, setEntries] = useState(mockContextEntries);
  const [content, setContent] = useState("");
  const [sourceType, setSourceType] = useState(sourceTypes[0]);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!content.trim()) return;
    setEntries([
      {
        id: (entries.length + 1).toString(),
        content,
        sourceType: sourceType as "WhatsApp" | "Email" | "Note",
        createdAt: new Date().toISOString(),
      },
      ...entries,
    ]);
    setContent("");
    setSourceType(sourceTypes[0]);
  }

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Context Input & History</h1>
        <form onSubmit={handleSubmit} className="mb-6 space-y-4 bg-white dark:bg-gray-800 p-4 rounded-lg shadow border border-gray-100 dark:border-gray-700">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Content</label>
            <textarea
              className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={2}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Source Type</label>
            <select
              className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              value={sourceType}
              onChange={(e) => setSourceType(e.target.value)}
            >
              {sourceTypes.map((type) => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
          <div className="flex justify-end">
            <button type="submit" className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Add Context</button>
          </div>
        </form>
        <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-100">Context History</h2>
        <div className="space-y-4">
          {entries.map((entry) => (
            <div key={entry.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 border border-gray-100 dark:border-gray-700">
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-blue-700 dark:text-blue-300">{entry.sourceType}</span>
                <span className="text-xs text-gray-500 dark:text-gray-400">{new Date(entry.createdAt).toLocaleString()}</span>
              </div>
              <div className="text-gray-900 dark:text-gray-100">{entry.content}</div>
              {entry.processedInsights && (
                <div className="mt-2 text-xs text-green-700 dark:text-green-300">AI Insight: {entry.processedInsights}</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </main>
  );
} 