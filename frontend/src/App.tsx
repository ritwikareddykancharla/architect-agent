import { useState } from 'react';
import axios from 'axios';
import { Terminal, Play, AlertCircle, CheckCircle2 } from 'lucide-react';

interface FixResponse {
  fixed_code: string;
  explanation: string;
}

function App() {
  const [code, setCode] = useState('');
  const [errorLog, setErrorLog] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<FixResponse | null>(null);

  const handleFix = async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.post('/api/fix', {
        code,
        error_log: errorLog
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert('Failed to fix code. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', padding: '2rem', gap: '1rem', boxSizing: 'border-box' }}>
      <header style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
        <div style={{ background: '#3b82f6', padding: '0.5rem', borderRadius: '0.5rem' }}>
          <Terminal color="white" size={24} />
        </div>
        <div style={{ textAlign: 'left' }}>
          <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>The Architect</h1>
          <p style={{ margin: 0, color: '#666' }}>Autonomous Code Repair Agent</p>
        </div>
      </header>

      <div style={{ display: 'flex', flex: 1, gap: '2rem' }}>
        {/* Left Panel: Input */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', background: 'white', padding: '1rem', borderRadius: '0.75rem', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}>
            <label style={{ fontWeight: 'bold', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <AlertCircle size={16} /> Broken Code
            </label>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste your broken code here..."
              style={{ flex: 1, width: '100%', padding: '0.5rem', borderRadius: '0.5rem', border: '1px solid #e5e7eb', fontFamily: 'monospace' }}
            />
          </div>

          <div style={{ height: '150px', display: 'flex', flexDirection: 'column', background: 'white', padding: '1rem', borderRadius: '0.75rem', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}>
            <label style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Error Log (Optional)</label>
            <textarea
              value={errorLog}
              onChange={(e) => setErrorLog(e.target.value)}
              placeholder="Paste stack trace or error message..."
              style={{ flex: 1, width: '100%', padding: '0.5rem', borderRadius: '0.5rem', border: '1px solid #e5e7eb', fontFamily: 'monospace' }}
            />
          </div>

          <button
            onClick={handleFix}
            disabled={loading || !code}
            style={{
              padding: '1rem',
              background: loading ? '#93c5fd' : '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '0.5rem',
              fontWeight: 'bold',
              cursor: loading ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
              fontSize: '1.1rem'
            }}
          >
            {loading ? 'Analyzing...' : <><Play size={20} /> Fix Code</>}
          </button>
        </div>

        {/* Right Panel: Output */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', background: 'white', padding: '1rem', borderRadius: '0.75rem', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}>
          <label style={{ fontWeight: 'bold', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <CheckCircle2 size={16} color={result ? "green" : "gray"} /> Fixed Result
          </label>
          {result ? (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '1rem', overflow: 'auto' }}>
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', borderLeft: '4px solid #4ade80' }}>
                <strong>Analysis:</strong>
                <p style={{ margin: '0.5rem 0 0 0' }}>{result.explanation}</p>
              </div>
              <pre style={{ flex: 1, background: '#1e293b', color: '#f8fafc', padding: '1rem', borderRadius: '0.5rem', overflow: 'auto', margin: 0 }}>
                <code>{result.fixed_code}</code>
              </pre>
            </div>
          ) : (
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#9ca3af' }}>
              Waiting for input...
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
