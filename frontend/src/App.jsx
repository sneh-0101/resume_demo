import React, { useState } from 'react'

export default function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    const fd = new FormData()
    fd.append('file', file)
    try {
      const res = await fetch('http://localhost:8000/match', {
        method: 'POST',
        body: fd,
      })
      const json = await res.json()
      setResult(json)
    } catch (err) {
      setResult({ error: err.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 720, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>Resume Matcher</h1>
      <form onSubmit={submit}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit" disabled={loading} style={{ marginLeft: 8 }}>
          {loading ? 'Matching...' : 'Upload & Match'}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h2>Result</h2>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
