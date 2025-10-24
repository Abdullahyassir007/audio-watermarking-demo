import { Link } from 'react-router-dom';

interface HomePageProps {
  isAuthenticated: boolean;
}

export default function HomePage({ isAuthenticated }: HomePageProps) {
  return (
    <div className="flex-1">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 text-white">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="container mx-auto px-4 py-24 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-block mb-6">
              <div className="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center text-5xl mx-auto shadow-2xl">
                🎵
              </div>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              Embed Hidden Messages in Audio
            </h1>
            <p className="text-xl md:text-2xl text-blue-100 mb-8 leading-relaxed">
              SilentCipher uses advanced watermarking technology to hide messages in audio files. 
              Secure, robust, and completely imperceptible to the human ear.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              {isAuthenticated ? (
                <>
                  <Link
                    to="/encode"
                    className="px-8 py-4 bg-white text-blue-600 font-semibold rounded-xl hover:bg-gray-100 transition-all shadow-xl hover:shadow-2xl transform hover:scale-105"
                  >
                    Start Encoding →
                  </Link>
                  <Link
                    to="/decode"
                    className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-xl hover:bg-white/20 transition-all border-2 border-white/30"
                  >
                    Decode Audio
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="px-8 py-4 bg-white text-blue-600 font-semibold rounded-xl hover:bg-gray-100 transition-all shadow-xl hover:shadow-2xl transform hover:scale-105"
                  >
                    Get Started →
                  </Link>
                  <Link
                    to="/about"
                    className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-xl hover:bg-white/20 transition-all border-2 border-white/30"
                  >
                    Learn More
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
        {/* Wave decoration */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z" fill="white"/>
          </svg>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Powerful Features</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need to securely watermark your audio files
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Feature 1 */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 border border-blue-100 hover:shadow-xl transition-all transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center text-3xl mb-6 shadow-lg">
                🔒
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Secure Encoding</h3>
              <p className="text-gray-600 leading-relaxed">
                Embed messages that are cryptographically secure and resistant to tampering. Your data stays protected.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 border border-purple-100 hover:shadow-xl transition-all transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl flex items-center justify-center text-3xl mb-6 shadow-lg">
                🎧
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Imperceptible</h3>
              <p className="text-gray-600 leading-relaxed">
                Watermarks are completely inaudible. Your audio quality remains pristine and unaffected.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-8 border border-green-100 hover:shadow-xl transition-all transform hover:scale-105">
              <div className="w-16 h-16 bg-gradient-to-br from-green-600 to-emerald-600 rounded-xl flex items-center justify-center text-3xl mb-6 shadow-lg">
                💪
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Robust</h3>
              <p className="text-gray-600 leading-relaxed">
                Watermarks survive compression, noise, and other distortions. Reliable detection every time.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Simple three-step process to watermark your audio
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Step 1 */}
              <div className="text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-full flex items-center justify-center text-3xl font-bold text-white mx-auto mb-6 shadow-xl">
                  1
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">Upload Audio</h3>
                <p className="text-gray-600">
                  Select your audio file and the message you want to embed
                </p>
              </div>

              {/* Step 2 */}
              <div className="text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center text-3xl font-bold text-white mx-auto mb-6 shadow-xl">
                  2
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">Encode</h3>
                <p className="text-gray-600">
                  Our algorithm embeds your message imperceptibly into the audio
                </p>
              </div>

              {/* Step 3 */}
              <div className="text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-green-600 to-emerald-600 rounded-full flex items-center justify-center text-3xl font-bold text-white mx-auto mb-6 shadow-xl">
                  3
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">Download</h3>
                <p className="text-gray-600">
                  Get your watermarked audio file, ready to share or distribute
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      {!isAuthenticated && (
        <section className="py-20 bg-gradient-to-br from-blue-600 to-indigo-600 text-white">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl font-bold mb-6">Ready to Get Started?</h2>
            <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Join thousands of users protecting their audio content with SilentCipher
            </p>
            <Link
              to="/login"
              className="inline-block px-8 py-4 bg-white text-blue-600 font-semibold rounded-xl hover:bg-gray-100 transition-all shadow-xl hover:shadow-2xl transform hover:scale-105"
            >
              Sign Up Now →
            </Link>
          </div>
        </section>
      )}
    </div>
  );
}
