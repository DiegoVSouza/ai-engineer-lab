# Bounded metadata retry

Retry only read-only catalog transport failures on the same credential, up to three total attempts, with bounded jitter and timeout. Never rotate on failures or replay completions, quota or HTTP authorization errors.
