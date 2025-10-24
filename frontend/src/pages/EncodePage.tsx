import { useState } from 'react';
import MessageInput from '../components/MessageInput';
import type { MessagePayload } from '../types/message';

export default function EncodePage() {
  const [currentMessage, setCurrentMessage] = useState<MessagePayload | null>(null);

  const handleMessageChange = (message: MessagePayload) => {
    setCurrentMessage(message);
    console.log('Message updated:', message);
  };

  return (
    <div className="flex-1 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Encode Audio</h1>
            <p className="text-xl text-gray-600">
              Embed a hidden message into your audio file
            </p>
          </div>

          {/* Message Input */}
          <MessageInput onMessageChange={handleMessageChange} />

          {/* Audio Upload Section - Placeholder */}
          <div className="mt-8 bg-white rounded-2xl shadow-xl border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Upload Audio File</h2>
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-blue-500 transition-colors cursor-pointer">
              <div className="text-6xl mb-4">🎵</div>
              <p className="text-lg font-medium text-gray-700 mb-2">
                Drag and drop your audio file here
              </p>
              <p className="text-sm text-gray-500 mb-4">
                or click to browse (WAV, MP3, FLAC, OGG)
              </p>
              <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all shadow-md">
                Select File
              </button>
            </div>
          </div>

          {/* Encode Button - Placeholder */}
          <div className="mt-8 text-center">
            <button
              disabled
              className="px-12 py-4 bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold text-lg rounded-xl hover:from-green-600 hover:to-emerald-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              🔒 Encode Message
            </button>
            <p className="text-sm text-gray-500 mt-4">
              Audio upload component will be implemented in the next task
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
