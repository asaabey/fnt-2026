#!/usr/bin/env python3
"""Verify the public HTTPS copies and caching; never use Cloudflare credentials."""
from pathlib import Path
from datetime import datetime,timezone
import concurrent.futures,hashlib,json,urllib.request,subprocess,tempfile
root=Path(__file__).resolve().parent
config=json.loads((root/'assets.json').read_text())
def verify(asset):
    attempts=[]
    for _ in range(2):
        try:
            request=urllib.request.Request(asset['url'],headers={'User-Agent':'FimbriaAssetCheck/1.0'})
            with urllib.request.urlopen(request,timeout=25) as response:
                data=response.read()
                attempts.append({'status':response.status,'bytes':len(data),
                    'sha256Matches':hashlib.sha256(data).hexdigest()==asset['sha256'],
                    'contentType':response.headers.get('content-type'),
                    'cacheControl':response.headers.get('cache-control'),
                    'cfCacheStatus':response.headers.get('cf-cache-status'),
                    'age':response.headers.get('age')})
        except Exception as error:
            # A new hostname can remain negatively cached by the local resolver.
            # Verify through public DNS-over-HTTPS without disabling TLS checks.
            with tempfile.TemporaryDirectory(prefix='fimbria-asset-check-') as directory:
                headers=Path(directory)/'headers.txt';body=Path(directory)/'body'
                result=subprocess.run(['curl','--silent','--show-error','--fail',
                    '--max-time','25','--doh-url','https://cloudflare-dns.com/dns-query',
                    '--dump-header',str(headers),'--output',str(body),asset['url']],
                    capture_output=True,text=True)
                if result.returncode==0:
                    lines=headers.read_text().splitlines();values={}
                    for line in lines:
                        if ':' in line:
                            key,value=line.split(':',1);values[key.lower()]=value.strip()
                    status=int(next(line.split()[1] for line in reversed(lines) if line.startswith('HTTP/')))
                    data=body.read_bytes()
                    attempts.append({'status':status,'bytes':len(data),
                        'sha256Matches':hashlib.sha256(data).hexdigest()==asset['sha256'],
                        'contentType':values.get('content-type'),'cacheControl':values.get('cache-control'),
                        'cfCacheStatus':values.get('cf-cache-status'),'age':values.get('age'),
                        'dnsMode':'Cloudflare DNS-over-HTTPS; TLS verification enabled',
                        'localResolverError':str(error)})
                else:
                    attempts.append({'error':str(error),'publicDnsCheckError':result.stderr.strip()})
    return {'url':asset['url'],'requests':attempts}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    checks=list(executor.map(verify,config['assets']))
report={'checkedAt':datetime.now(timezone.utc).isoformat(),'checks':checks,
        'allPublicHttpsAndHashesPassed':all(all(r.get('status')==200 and r.get('sha256Matches') for r in a['requests']) for a in checks),
        'imagesHaveCacheHit':all(any(r.get('cfCacheStatus')=='HIT' for r in a['requests']) for a in checks if a['url'].endswith(('.webp','.png','.jpg','.jpeg')))}
(root/'http-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['allPublicHttpsAndHashesPassed'] and report['imagesHaveCacheHit'] else 1)
