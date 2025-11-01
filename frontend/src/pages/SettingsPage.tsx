import React, { useState } from 'react';
import { CheckCircle, AlertCircle, Key, Settings as SettingsIcon } from 'lucide-react';

export default function SettingsPage() {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // In a real app, you'd save this to your backend or secure storage
    localStorage.setItem('openai_api_key', apiKey);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleClear = () => {
    setApiKey('');
    localStorage.removeItem('openai_api_key');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center">
          <SettingsIcon className="w-6 h-6 mr-2" />
          Settings
        </h1>
        <p className="mt-1 text-sm text-gray-600">
          Configure your API keys and preferences
        </p>
      </div>

      {/* OpenAI Configuration */}
      <div className="card">
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center">
            <Key className="w-5 h-5 mr-2" />
            OpenAI API Configuration
          </h2>
          <p className="mt-1 text-sm text-gray-600">
            Configure your OpenAI API key to enable AI-powered keyword generation and prompt building
          </p>
        </div>

        <div className="space-y-4">
          <div>
            <label htmlFor="apiKey" className="block text-sm font-medium text-gray-700">
              API Key
            </label>
            <div className="mt-1 relative">
              <input
                type={showKey ? 'text' : 'password'}
                id="apiKey"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="input-field pr-10"
                placeholder="sk-..."
              />
              <button
                type="button"
                onClick={() => setShowKey(!showKey)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <span className="text-sm text-gray-500">
                  {showKey ? 'Hide' : 'Show'}
                </span>
              </button>
            </div>
            <p className="mt-1 text-xs text-gray-500">
              Your API key is stored locally and never sent to our servers
            </p>
          </div>

          <div className="flex items-center space-x-4">
            <button
              onClick={handleSave}
              disabled={!apiKey.trim()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {saved ? (
                <>
                  <CheckCircle className="w-4 h-4 mr-2" />
                  Saved
                </>
              ) : (
                'Save API Key'
              )}
            </button>
            <button
              onClick={handleClear}
              className="btn-secondary"
            >
              Clear
            </button>
          </div>
        </div>

        {/* Status */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <AlertCircle className="h-5 w-5 text-blue-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">
                API Key Status
              </h3>
              <div className="mt-2 text-sm text-blue-700">
                <p>
                  {apiKey ? (
                    <>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 mr-2">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Configured
                      </span>
                      AI-powered features are enabled
                    </>
                  ) : (
                    <>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 mr-2">
                        <AlertCircle className="w-3 h-3 mr-1" />
                        Not Configured
                      </span>
                      Using fallback stub implementations
                    </>
                  )}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          How to Get Your OpenAI API Key
        </h3>
        <div className="space-y-4">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-medium">
              1
            </div>
            <div>
              <p className="text-sm text-gray-700">
                Visit <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:text-primary-700">OpenAI Platform</a>
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-medium">
              2
            </div>
            <div>
              <p className="text-sm text-gray-700">
                Sign in or create an account
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-medium">
              3
            </div>
            <div>
              <p className="text-sm text-gray-700">
                Click "Create new secret key" and copy the key
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-medium">
              4
            </div>
            <div>
              <p className="text-sm text-gray-700">
                Paste the key above and click "Save API Key"
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}




