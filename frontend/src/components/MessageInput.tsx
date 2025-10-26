import { useState, useEffect } from 'react';
import type { MessagePayload, MessageFormat } from '../types/message';

interface MessageInputProps {
  onMessageChange: (message: MessagePayload) => void;
  messageType?: MessageFormat;
}

export default function MessageInput({ onMessageChange, messageType: initialType = 'numeric' }: MessageInputProps) {
  const [messageType, setMessageType] = useState<MessageFormat>(initialType);
  const [numericValues, setNumericValues] = useState<number[]>([0, 0, 0, 0, 0]);
  const [textValue, setTextValue] = useState<string>('');
  const [binaryValue, setBinaryValue] = useState<string>('');
  const [errors, setErrors] = useState<string[]>([]);
  const [currentPayload, setCurrentPayload] = useState<number[]>([0, 0, 0, 0, 0]);

  // Validate numeric input
  const validateNumeric = (values: number[]): boolean => {
    const newErrors: string[] = [];

    if (values.length !== 5) {
      newErrors.push('Must have exactly 5 values');
      setErrors(newErrors);
      return false;
    }

    values.forEach((val, idx) => {
      if (isNaN(val)) {
        newErrors.push(`Value ${idx + 1} must be a number`);
      } else if (val < 0 || val > 255) {
        newErrors.push(`Value ${idx + 1} must be between 0 and 255`);
      } else if (!Number.isInteger(val)) {
        newErrors.push(`Value ${idx + 1} must be an integer`);
      }
    });

    setErrors(newErrors);
    return newErrors.length === 0;
  };

  // Convert text to numeric payload
  const convertTextToPayload = (text: string): number[] => {
    // Simple conversion: take first 5 characters and convert to ASCII codes
    // Pad with zeros if less than 5 characters
    const values: number[] = [];
    for (let i = 0; i < 5; i++) {
      if (i < text.length) {
        values.push(text.charCodeAt(i) % 256);
      } else {
        values.push(0);
      }
    }
    return values;
  };

  // Convert binary string to numeric payload
  const convertBinaryToPayload = (binary: string): { values: number[], errors: string[] } => {
    // Remove any whitespace
    const cleanBinary = binary.replace(/\s/g, '');

    // Empty string is valid (returns zeros)
    if (cleanBinary === '') {
      return { values: [0, 0, 0, 0, 0], errors: [] };
    }

    // Validate binary string
    if (!/^[01]*$/.test(cleanBinary)) {
      return { values: [0, 0, 0, 0, 0], errors: ['Binary string must contain only 0s and 1s'] };
    }

    if (cleanBinary.length !== 40) {
      return {
        values: [0, 0, 0, 0, 0],
        errors: [`Binary string must be exactly 40 bits (currently ${cleanBinary.length})`]
      };
    }

    // Convert 40 bits to 5 bytes (8 bits each)
    const values: number[] = [];
    for (let i = 0; i < 5; i++) {
      const byte = cleanBinary.substring(i * 8, (i + 1) * 8);
      values.push(parseInt(byte, 2));
    }

    return { values, errors: [] };
  };

  // Generate random message
  const generateRandom = () => {
    const randomValues = Array.from({ length: 5 }, () => Math.floor(Math.random() * 256));
    setNumericValues(randomValues);
    setErrors([]);

    // Emit the random message
    const payload: MessagePayload = {
      format: 'numeric',
      values: randomValues,
      originalInput: randomValues,
    };
    onMessageChange(payload);
  };

  // Handle numeric value change
  const handleNumericChange = (index: number, value: string) => {
    const numValue = value === '' ? 0 : parseInt(value, 10);
    const newValues = [...numericValues];
    newValues[index] = numValue;
    setNumericValues(newValues);

    if (validateNumeric(newValues)) {
      const payload: MessagePayload = {
        format: 'numeric',
        values: newValues,
        originalInput: newValues,
      };
      onMessageChange(payload);
    }
  };

  // Handle text change
  const handleTextChange = (value: string) => {
    // Limit to 5 characters for simplicity
    const limitedValue = value.substring(0, 5);
    setTextValue(limitedValue);

    const numericValues = convertTextToPayload(limitedValue);
    const payload: MessagePayload = {
      format: 'text',
      values: numericValues,
      originalInput: limitedValue,
    };
    onMessageChange(payload);
  };

  // Handle binary change
  const handleBinaryChange = (value: string) => {
    setBinaryValue(value);

    const result = convertBinaryToPayload(value);
    setErrors(result.errors);
    setCurrentPayload(result.values);

    if (result.errors.length === 0) {
      const payload: MessagePayload = {
        format: 'binary',
        values: result.values,
        originalInput: value,
      };
      onMessageChange(payload);
    }
  };

  // Handle format switch
  const handleFormatSwitch = (newFormat: MessageFormat) => {
    setMessageType(newFormat);
    setErrors([]);

    // Emit current values in new format
    let payload: MessagePayload;
    switch (newFormat) {
      case 'numeric':
        setCurrentPayload(numericValues);
        payload = {
          format: 'numeric',
          values: numericValues,
          originalInput: numericValues,
        };
        break;
      case 'text':
        const textValues = convertTextToPayload(textValue);
        setCurrentPayload(textValues);
        payload = {
          format: 'text',
          values: textValues,
          originalInput: textValue,
        };
        break;
      case 'binary':
        const result = convertBinaryToPayload(binaryValue);
        setCurrentPayload(result.values);
        setErrors(result.errors);
        payload = {
          format: 'binary',
          values: result.values,
          originalInput: binaryValue,
        };
        break;
    }
    onMessageChange(payload);
  };

  // Update current payload when switching modes
  useEffect(() => {
    setCurrentPayload(numericValues);
  }, [numericValues]);

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-6">
          <h2 className="text-3xl font-bold text-white mb-2">Message Input</h2>
          <p className="text-blue-100 text-sm">Choose your input format and enter your watermark message</p>
        </div>

        <div className="p-8">
          {/* Format Tabs */}
          <div className="flex gap-2 mb-8 bg-gray-100 p-1.5 rounded-xl">
            <button
              onClick={() => handleFormatSwitch('numeric')}
              className={`flex-1 px-6 py-3 font-semibold rounded-lg transition-all duration-200 ${messageType === 'numeric'
                ? 'bg-white text-blue-600 shadow-md transform scale-105'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
            >
              <div className="flex items-center justify-center gap-2">
                <span className="text-xl">🔢</span>
                <span>Numeric</span>
              </div>
            </button>
            <button
              onClick={() => handleFormatSwitch('text')}
              className={`flex-1 px-6 py-3 font-semibold rounded-lg transition-all duration-200 ${messageType === 'text'
                ? 'bg-white text-blue-600 shadow-md transform scale-105'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
            >
              <div className="flex items-center justify-center gap-2">
                <span className="text-xl">📝</span>
                <span>Text</span>
              </div>
            </button>
            <button
              onClick={() => handleFormatSwitch('binary')}
              className={`flex-1 px-6 py-3 font-semibold rounded-lg transition-all duration-200 ${messageType === 'binary'
                ? 'bg-white text-blue-600 shadow-md transform scale-105'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
            >
              <div className="flex items-center justify-center gap-2">
                <span className="text-xl">💾</span>
                <span>Binary</span>
              </div>
            </button>
          </div>

          {/* Input Area */}
          <div className="bg-white rounded-xl p-6 border-2 border-gray-200 mb-6">
            {/* Numeric Input */}
            {messageType === 'numeric' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800">Numeric Array Input</h3>
                    <p className="text-sm text-gray-500 mt-1">Enter 5 integers between 0-255</p>
                  </div>
                  <button
                    onClick={generateRandom}
                    className="px-5 py-2.5 bg-gradient-to-r from-green-500 to-emerald-500 text-white font-medium rounded-lg hover:from-green-600 hover:to-emerald-600 transition-all duration-200 shadow-md hover:shadow-lg transform hover:scale-105 flex items-center gap-2"
                  >
                    <span>🎲</span>
                    <span>Random</span>
                  </button>
                </div>
                <div className="grid grid-cols-5 gap-4">
                  {numericValues.map((value, index) => (
                    <div key={index} className="relative">
                      <label className="block text-xs font-medium text-gray-600 mb-2">
                        Byte {index + 1}
                      </label>
                      <input
                        type="number"
                        min="0"
                        max="255"
                        value={value}
                        onChange={(e) => handleNumericChange(index, e.target.value)}
                        className="w-full px-4 py-3 text-center text-lg font-mono border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                        placeholder="0"
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Text Input */}
            {messageType === 'text' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">Text Input</h3>
                  <p className="text-sm text-gray-500 mt-1">Enter up to 5 characters (converted to ASCII)</p>
                </div>
                <div className="relative">
                  <input
                    type="text"
                    maxLength={5}
                    value={textValue}
                    onChange={(e) => handleTextChange(e.target.value)}
                    className="w-full px-6 py-4 text-xl border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="Type here..."
                  />
                  <div className="absolute right-4 top-1/2 -translate-y-1/2 bg-gray-100 px-3 py-1 rounded-full">
                    <span className="text-sm font-medium text-gray-600">
                      {textValue.length}/5
                    </span>
                  </div>
                </div>
                {textValue && (
                  <div className="flex gap-2 flex-wrap">
                    {textValue.split('').map((char, idx) => (
                      <div key={idx} className="bg-blue-50 px-4 py-2 rounded-lg border border-blue-200">
                        <div className="text-xs text-gray-500">Char {idx + 1}</div>
                        <div className="text-lg font-mono font-bold text-blue-600">{char}</div>
                        <div className="text-xs text-gray-500">ASCII: {char.charCodeAt(0)}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Binary Input */}
            {messageType === 'binary' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">Binary Input</h3>
                  <p className="text-sm text-gray-500 mt-1">Enter exactly 40 bits (5 bytes × 8 bits)</p>
                </div>
                <div className="relative">
                  <textarea
                    value={binaryValue}
                    onChange={(e) => handleBinaryChange(e.target.value)}
                    className="w-full px-6 py-4 text-lg font-mono border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
                    placeholder="00000000 00000000 00000000 00000000 00000000"
                    rows={4}
                  />
                  <div className="absolute right-4 top-4 bg-gray-100 px-3 py-1 rounded-full">
                    <span className={`text-sm font-medium ${binaryValue.replace(/\s/g, '').length === 40 ? 'text-green-600' : 'text-gray-600'
                      }`}>
                      {binaryValue.replace(/\s/g, '').length}/40 bits
                    </span>
                  </div>
                </div>
                {binaryValue && binaryValue.replace(/\s/g, '').length === 40 && (
                  <div className="grid grid-cols-5 gap-2">
                    {Array.from({ length: 5 }).map((_, idx) => {
                      const start = idx * 8;
                      const byte = binaryValue.replace(/\s/g, '').substring(start, start + 8);
                      return (
                        <div key={idx} className="bg-green-50 px-3 py-2 rounded-lg border border-green-200 text-center">
                          <div className="text-xs text-gray-500">Byte {idx + 1}</div>
                          <div className="text-sm font-mono font-bold text-green-600">{byte}</div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Error Display */}
          {errors.length > 0 && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
              <div className="flex items-start gap-3">
                <span className="text-2xl">⚠️</span>
                <div className="flex-1">
                  <p className="text-sm font-semibold text-red-800 mb-2">Validation Error</p>
                  <ul className="space-y-1">
                    {errors.map((error, index) => (
                      <li key={index} className="text-sm text-red-700">{error}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Current Values Display */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-2xl">📊</span>
              <h3 className="text-lg font-semibold text-gray-800">Payload Preview</h3>
            </div>
            <div className="grid grid-cols-5 gap-3">
              {currentPayload.map((val, idx) => (
                <div key={idx} className="bg-white rounded-lg p-4 border-2 border-blue-200 text-center transform transition-all hover:scale-105">
                  <div className="text-xs font-medium text-gray-500 mb-1">Byte {idx + 1}</div>
                  <div className="text-2xl font-bold text-blue-600 font-mono">{val}</div>
                  <div className="text-xs text-gray-400 mt-1">{val.toString(16).toUpperCase().padStart(2, '0')}h</div>
                </div>
              ))}
            </div>
            <div className="mt-4 pt-4 border-t border-blue-200">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Total Bytes:</span>
                <span className="font-mono font-semibold text-gray-800">5 bytes (40 bits)</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
