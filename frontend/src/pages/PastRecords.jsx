import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { appointmentAPI } from '../services/api';
import './PastRecords.css';

const prettyStatus = (status) => (status || 'unknown').replaceAll('_', ' ').replace(/\\b\\w/g, c => c.toUpperCase());

function PastRecords() {
  const navigate = useNavigate();
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    let active = true;
    appointmentAPI.getAll()
      .then(({ data }) => {
        if (active) {
          const all = Array.isArray(data?.appointments) ? data.appointments : [];
          const today = new Date(); today.setHours(0, 0, 0, 0);
          const history = all.filter(item => {
            const date = item.appointment_date ? new Date(`${item.appointment_date}T00:00:00`) : null;
            return ['completed', 'cancelled'].includes((item.status || '').toLowerCase()) ||
              (date && !Number.isNaN(date.getTime()) && date < today);
          });
          history.sort((a, b) => new Date(b.appointment_date) - new Date(a.appointment_date));
          setRecords(history);
        }
      })
      .catch(err => {
        if (active) setError(err.response?.data?.message || err.response?.data?.error || 'Unable to load visit history. Please try again.');
      })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);

  const filtered = useMemo(() => records.filter(item => {
    const matchesStatus = filter === 'all' || item.status === filter;
    const haystack = [item.hospital_name, item.doctor_name, item.doctor_specialty, item.reason, item.id].join(' ').toLowerCase();
    return matchesStatus && haystack.includes(query.toLowerCase());
  }), [records, filter, query]);

  const completed = records.filter(item => item.status === 'completed').length;
  const cancelled = records.filter(item => item.status === 'cancelled').length;

  if (loading) return <main className="container"><div className="history-loading">Loading your visit history…</div></main>;

  return (
    <main className="container history-page">
      <button 
        onClick={() => navigate('/dashboard')} 
        className="btn btn-outline" 
        style={{ marginBottom: '1rem' }}
      >
        ← Back to Dashboard
      </button>
      
      <header className="history-hero">
        <div>
          <span className="eyebrow">YOUR CARE JOURNEY</span>
          <h1>Past records</h1>
          <p>A clear timeline of your previous appointments and healthcare visits.</p>
        </div>
        <div className="history-mark" aria-hidden="true">✚</div>
      </header>

      <section className="history-stats" aria-label="Visit history summary">
        <article className="history-stat"><span>Total past visits</span><strong>{records.length}</strong></article>
        <article className="history-stat"><span>Completed</span><strong>{completed}</strong></article>
        <article className="history-stat"><span>Cancelled</span><strong>{cancelled}</strong></article>
      </section>

      <section className="history-controls">
        <label className="history-search"><span className="sr-only">Search records</span><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search hospital, doctor or speciality…" /></label>
        <div className="history-filters" role="group" aria-label="Filter records">
          {[['all','All records'],['completed','Completed'],['cancelled','Cancelled']].map(([value,label]) =>
            <button key={value} className={filter === value ? 'selected' : ''} onClick={() => setFilter(value)}>{label}</button>
          )}
        </div>
      </section>

      {error && <div className="history-error" role="alert">{error}</div>}
      {!error && filtered.length === 0 && (
        <div className="history-empty"><div>▤</div><h2>No past records found</h2><p>Completed and cancelled appointments will appear here after they are recorded.</p></div>
      )}

      <section className="history-list" aria-label="Previous appointments">
        {filtered.map(item => (
          <article className="history-record" key={item.id}>
            <div className="history-date"><strong>{item.appointment_date ? new Date(`${item.appointment_date}T00:00:00`).toLocaleDateString(undefined,{day:'2-digit'}) : '—'}</strong><span>{item.appointment_date ? new Date(`${item.appointment_date}T00:00:00`).toLocaleDateString(undefined,{month:'short',year:'numeric'}) : 'Date unavailable'}</span></div>
            <div className="history-record-main">
              <div className="history-record-top"><h2>{item.hospital_name || 'Healthcare facility'}</h2><span className={`history-status ${item.status === 'completed' ? 'is-complete' : 'is-cancelled'}`}>{prettyStatus(item.status)}</span></div>
              <p className="history-doctor">{item.doctor_name || 'Doctor not recorded'}{item.doctor_specialty ? ` · ${item.doctor_specialty}` : ''}</p>
              <div className="history-meta"><span>◷ {item.appointment_time || 'Time not recorded'}</span>{item.reason && <span>Reason: {item.reason}</span>}<span>Visit ID: #{item.id}</span></div>
              {item.notes && <p className="history-notes">{item.notes}</p>}
              {(item.documents_required?.length > 0 || item.documents_submitted?.length > 0) && <p className="history-docs">Documents: {item.documents_submitted?.length || 0} submitted / {item.documents_required?.length || 0} required</p>}
            </div>
          </article>
        ))}
      </section>
      <p className="history-disclaimer">This history reflects appointment records stored in this application. It is not a substitute for an official hospital medical record.</p>
    </main>
  );
}

export default PastRecords;
