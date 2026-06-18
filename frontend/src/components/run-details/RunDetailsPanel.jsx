import { useEffect, useState } from 'react';
import { getModelRun } from '../../api/runApi.js';

function RunDetailsPanel({ details }) {
  const [fullDetails, setFullDetails] = useState(null);
  const isGuestRun = details?.request_id === 'guest';

  // Loads full model run metadata after the streaming endpoint returns a run ID.
  useEffect(() => {
    if (!details?.run_id || isGuestRun) {
      setFullDetails(details || null);
      return;
    }
    getModelRun(details.run_id)
      .then((data) => setFullDetails(data.run))
      .catch(() => setFullDetails(details));
  }, [details?.run_id, isGuestRun]);

  return (
    <aside className="bg-slate-900 p-4">
      <h2 className="font-semibold text-white">Run Details</h2>
      {fullDetails ? (
        <pre className="mt-4 overflow-auto rounded bg-slate-950 p-3 text-xs text-slate-300">{JSON.stringify(fullDetails, null, 2)}</pre>
      ) : (
        <p className="mt-4 text-sm text-slate-400">Send a message to see model run metadata.</p>
      )}
    </aside>
  );
}

export default RunDetailsPanel;
