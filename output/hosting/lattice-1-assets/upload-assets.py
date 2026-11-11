#!/usr/bin/env python3
"""Upload the reviewed asset manifest using the current Wrangler login."""
from pathlib import Path
import hashlib,json,subprocess
root=Path(__file__).resolve().parent
config=json.loads((root/'assets.json').read_text())
for asset in config['assets']:
    source=root/asset['file']
    if hashlib.sha256(source.read_bytes()).hexdigest()!=asset['sha256']:
        raise SystemExit('Hash mismatch: '+asset['file'])
    subprocess.run(['wrangler','r2','object','put',config['bucket']+'/'+asset['key'],
                    '--remote','--file',str(source),'--content-type',asset['contentType'],
                    '--cache-control',asset['cacheControl']],check=True)
    print('Uploaded: '+asset['url'],flush=True)
