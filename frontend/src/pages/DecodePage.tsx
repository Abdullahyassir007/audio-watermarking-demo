export default function DecodePage() {
  return (
    <div className="flex-1 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Decode Audio</h1>
            <p className="text-xl text-gray-600">
              Extract hidden messages from watermarked audio files
            </p>
          </div>

          {/* Audio Upload Section - Placeholder */}
          <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Upload Watermarked Audio</h2>
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-purple-500 transition-colors cursor-pointer">
              <div className="text-6xl mb-4">🔍</div>
              <p className="text-lg font-medium text-gray-700 mb-2">
                Drag and drop your watermarked audio file here
              </p>
              <p className="text-sm text-gray-500 mb-4">
                or click to browse (WAV, MP3, FLAC, OGG)
              </p>
              <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all shadow-md">
                Select File
              </button>
            </div>
          </div>

          {/* Decode Button - Placeholder */}
          <div className="mt-8 text-center">
            <button
              disabled
              className="px-12 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold text-lg rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              🔓 Decode Message
            </button>
            <p className="text-sm text-gray-500 mt-4">
              Audio upload and decoder components will be implemented in upcoming tasks
            </p>
          </div>

          {/* Results Placeholder */}
          <div className="mt-12 bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 border border-purple-200">
            <div className="text-center">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Decoded Message Will Appear Here</h3>
              <p className="text-gray-600">
                Upload and decode an audio file to see the extracted message
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
