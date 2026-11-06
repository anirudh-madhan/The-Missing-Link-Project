import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { constraintAPI } from '../services/api';
import './ConstraintLab.css';

function ConstraintLab({ language }) {
  const navigate = useNavigate();
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [testResult, setTestResult] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [testing, setTesting] = useState(false);

  useEffect(() => {
    fetchScenarios();
    fetchLogs();
  }, []);

  const fetchScenarios = async () => {
    try {
      const response = await constraintAPI.getAll();
      setScenarios(response.data.constraints);
    } catch (error) {
      console.error('Error fetching scenarios:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchLogs = async () => {
    try {
      const response = await constraintAPI.getLogs({ limit: 20 });
      setLogs(response.data.logs);
    } catch (error) {
      console.error('Error fetching logs:', error);
    }
  };

  const runTest = async (scenarioId) => {
    setTesting(true);
    setTestResult(null);
    setSelectedScenario(scenarioId);

    try {
      const response = await constraintAPI.runTest(scenarioId);
      setTestResult(response.data);
      await fetchLogs(); // Refresh logs
    } catch (error) {
      console.error('Error running test:', error);
      setTestResult({
        constraint_id: scenarioId,
        result: 'FAIL',
        system_response: 'Test execution failed',
        error: error.message
      });
    } finally {
      setTesting(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading Constraint Lab...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="constraint-lab">
        <button 
          onClick={() => navigate('/dashboard')} 
          className="btn btn-outline" 
          style={{ marginBottom: '1rem' }}
        >
          ← Back to Dashboard
        </button>
        
        <div className="lab-header">
          <h1>🔬 Constraint Lab</h1>
          <p>Test system resilience across 12 real-world healthcare scenarios</p>
        </div>

        <div className="lab-content">
          <div className="scenarios-panel">
            <h2>Test Scenarios (C01-C12)</h2>
            <div className="scenarios-list">
              {scenarios.map((scenario) => (
                <div
                  key={scenario.id}
                  className={`scenario-card ${selectedScenario === scenario.id ? 'active' : ''}`}
                >
                  <div className="scenario-header">
                    <h3>{scenario.id}: {scenario.name}</h3>
                    <button
                      onClick={() => runTest(scenario.id)}
                      className="btn btn-primary btn-small"
                      disabled={testing}
                    >
                      {testing && selectedScenario === scenario.id ? 'Running...' : 'Run Test'}
                    </button>
                  </div>
                  <p className="scenario-description">{scenario.description}</p>
                  <div className="scenario-test-case">
                    <strong>Test Case:</strong>
                    <p>{scenario.test_case}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {testResult && (
            <div className="result-panel">
              <h2>Test Results</h2>
              <div className={`result-card result-${testResult.result.toLowerCase()}`}>
                <div className="result-header">
                  <h3>{testResult.constraint_id}: {testResult.constraint_name}</h3>
                  <span className={`result-badge ${testResult.result === 'PASS' ? 'badge-success' : 'badge-error'}`}>
                    {testResult.result}
                  </span>
                </div>

                <div className="result-section">
                  <h4>📋 Test Case</h4>
                  <p>{testResult.test_case}</p>
                </div>

                <div className="result-section">
                  <h4>⚙️ System Response</h4>
                  <p>{testResult.system_response}</p>
                </div>

                {testResult.details && Object.keys(testResult.details).length > 0 && (
                  <div className="result-section">
                    <h4>📊 Details</h4>
                    <div className="details-grid">
                      {Object.entries(testResult.details).map(([key, value]) => (
                        <div key={key} className="detail-item">
                          <strong>{key.replace(/_/g, ' ')}:</strong>
                          <span>{typeof value === 'object' ? JSON.stringify(value) : String(value)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="result-meta">
                  <span>⏱️ Execution Time: {testResult.execution_time?.toFixed(3)}s</span>
                  <span>📅 {new Date(testResult.timestamp).toLocaleString()}</span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="audit-logs">
          <div className="flex-between mb-3">
            <h2>Audit Logs</h2>
            <div className="log-stats">
              <span className="stat">
                Total Tests: {logs.length}
              </span>
              <span className="stat stat-success">
                Pass: {logs.filter(l => l.result === 'PASS').length}
              </span>
              <span className="stat stat-error">
                Fail: {logs.filter(l => l.result === 'FAIL').length}
              </span>
            </div>
          </div>

          <div className="logs-table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Scenario</th>
                  <th>Result</th>
                  <th>Execution Time</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id}>
                    <td>{log.constraint_id}</td>
                    <td>{log.constraint_name}</td>
                    <td>
                      <span className={`badge ${log.result === 'PASS' ? 'badge-success' : 'badge-error'}`}>
                        {log.result}
                      </span>
                    </td>
                    <td>{log.execution_time?.toFixed(3)}s</td>
                    <td>{new Date(log.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ConstraintLab;
