function SourcesBlock({ sources }) {
  // Sources are collapsed by default to keep web-search answers readable.
  return (
    <details className="mb-3 rounded-lg border border-slate-700 p-3">
      <summary className="cursor-pointer text-sm font-medium text-blue-300">Sources</summary>
      <div className="mt-3 space-y-3">
        {sources.map((source, index) => (
          <div key={`${source.url}-${index}`} className="text-sm">
            <a href={source.url} target="_blank" rel="noreferrer" className="text-blue-400">{source.title}</a>
            <p className="text-slate-400">{source.snippet}</p>
          </div>
        ))}
      </div>
    </details>
  );
}

export default SourcesBlock;
