export default function AboutPage() {
  return (
    <div className="flex-1">
      {/* Hero */}
      <section className="bg-gradient-to-br from-blue-600 to-indigo-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">About SilentCipher</h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Advanced audio watermarking technology for secure message embedding
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="prose prose-lg max-w-none">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">What is SilentCipher?</h2>
            <p className="text-gray-600 leading-relaxed mb-6">
              SilentCipher is a cutting-edge audio watermarking platform that allows you to embed hidden messages 
              directly into audio files. Using advanced signal processing techniques, we ensure that your messages 
              remain imperceptible to listeners while being robust enough to survive various audio transformations.
            </p>

            <h2 className="text-3xl font-bold text-gray-900 mb-6 mt-12">Technology</h2>
            <p className="text-gray-600 leading-relaxed mb-6">
              Our watermarking system is built on state-of-the-art algorithms that operate in the frequency domain. 
              By carefully modifying specific frequency components, we can embed data that is:
            </p>
            <ul className="list-disc list-inside text-gray-600 space-y-2 mb-6">
              <li><strong>Imperceptible:</strong> The watermark doesn't affect audio quality</li>
              <li><strong>Robust:</strong> Survives compression, noise, and other distortions</li>
              <li><strong>Secure:</strong> Cryptographically protected against tampering</li>
              <li><strong>Efficient:</strong> Fast encoding and decoding processes</li>
            </ul>

            <h2 className="text-3xl font-bold text-gray-900 mb-6 mt-12">Use Cases</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
                <h3 className="text-xl font-bold text-gray-900 mb-3">🎵 Copyright Protection</h3>
                <p className="text-gray-600">
                  Embed ownership information in your audio content to prove authenticity and track distribution.
                </p>
              </div>
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-100">
                <h3 className="text-xl font-bold text-gray-900 mb-3">🔐 Secure Communication</h3>
                <p className="text-gray-600">
                  Send hidden messages through audio channels for covert communication applications.
                </p>
              </div>
              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6 border border-green-100">
                <h3 className="text-xl font-bold text-gray-900 mb-3">📊 Broadcast Monitoring</h3>
                <p className="text-gray-600">
                  Track when and where your audio content is played across different platforms.
                </p>
              </div>
              <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-xl p-6 border border-orange-100">
                <h3 className="text-xl font-bold text-gray-900 mb-3">🎬 Media Authentication</h3>
                <p className="text-gray-600">
                  Verify the integrity and origin of audio recordings in legal and forensic contexts.
                </p>
              </div>
            </div>

            <h2 className="text-3xl font-bold text-gray-900 mb-6 mt-12">Technical Specifications</h2>
            <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
              <ul className="space-y-3 text-gray-600">
                <li className="flex items-start gap-3">
                  <span className="text-blue-600 font-bold">•</span>
                  <span><strong>Supported Formats:</strong> WAV, MP3, FLAC, OGG</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-blue-600 font-bold">•</span>
                  <span><strong>Sample Rates:</strong> 16kHz, 44.1kHz, 48kHz</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-blue-600 font-bold">•</span>
                  <span><strong>Message Capacity:</strong> 5 bytes (40 bits) per watermark</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-blue-600 font-bold">•</span>
                  <span><strong>Encoding Time:</strong> ~2-5 seconds per minute of audio</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-blue-600 font-bold">•</span>
                  <span><strong>Detection Accuracy:</strong> 99%+ under normal conditions</span>
                </li>
              </ul>
            </div>

            <h2 className="text-3xl font-bold text-gray-900 mb-6 mt-12">Open Source</h2>
            <p className="text-gray-600 leading-relaxed mb-6">
              SilentCipher is built on open-source technologies and research. We believe in transparency 
              and community-driven development. Check out our GitHub repository to explore the code, 
              contribute improvements, or report issues.
            </p>
            <a
              href="#"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg hover:shadow-xl"
            >
              <span>View on GitHub</span>
              <span>→</span>
            </a>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Team</h2>
            <p className="text-xl text-gray-600">
              Built by researchers and engineers passionate about audio security
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-2xl p-6 text-center shadow-lg hover:shadow-xl transition-all">
                <div className="w-24 h-24 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-full mx-auto mb-4 flex items-center justify-center text-4xl text-white">
                  👤
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Team Member {i}</h3>
                <p className="text-gray-600 mb-4">Audio Engineer</p>
                <div className="flex gap-3 justify-center">
                  <a href="#" className="w-10 h-10 bg-gray-100 hover:bg-blue-600 hover:text-white rounded-lg flex items-center justify-center transition-colors">
                    🐦
                  </a>
                  <a href="#" className="w-10 h-10 bg-gray-100 hover:bg-blue-600 hover:text-white rounded-lg flex items-center justify-center transition-colors">
                    💼
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
