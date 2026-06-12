#!/usr/bin/env python3
"""STDD Experience Share API Server — GitHub API version, no git needed."""
import json, os, sys, requests
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from base64 import b64encode

GITHUB_REPO = 'leonai42/stdd-experiences'
PENDING_DIR = 'pending'
TOKEN_FILE = '/etc/stdd/github-token'
API_BASE = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{PENDING_DIR}'
PORT = 8800

def load_token():
    try:
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    except Exception:
        return None

def upload_to_github(exp_id, content):
    token = load_token()
    if not token:
        return False, 'token missing'
    url = f'{API_BASE}/{exp_id}.md'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
    }
    payload = {
        'message': f'share: {exp_id}',
        'content': b64encode(content.encode('utf-8')).decode('ascii'),
        'branch': 'main',
    }
    # Check if file already exists (for update)
    r = requests.get(url, headers=headers, timeout=20)
    if r.status_code == 200:
        payload['sha'] = r.json()['sha']
    r = requests.put(url, json=payload, headers=headers, timeout=30)
    if r.status_code in (200, 201):
        return True, r.json().get('commit', {}).get('sha', 'ok')
    return False, r.json().get('message', f'HTTP {r.status_code}')[:500]

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/api/share-experience':
            self.send_error(404); return
        try:
            n = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(n))
            eid = data.get('experience_id', '')
            content = data.get('content', '')
            if not eid or not content:
                self._j({'success': False, 'error': 'missing experience_id or content'}); return
            if len(content) < 50:
                self._j({'success': False, 'error': 'content too short'}); return
            ok, msg = upload_to_github(eid, content)
            if not ok:
                self._j({'success': False, 'error': f'upload failed: {msg}'}); return
            self._j({'success': True, 'experience_id': eid, 'message': 'submitted to pending'})
        except json.JSONDecodeError:
            self._j({'success': False, 'error': 'invalid JSON'})
        except Exception as e:
            self._j({'success': False, 'error': str(e)[:500]})

    def do_GET(self):
        if self.path == '/api/health':
            self._j({'status': 'ok', 'time': datetime.now().isoformat()})
        else:
            self.send_error(404)

    def _j(self, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f'[{datetime.now().isoformat()}] {args[0]}')

def main():
    s = HTTPServer(('127.0.0.1', PORT), H)
    print(f'STDD Share API on 127.0.0.1:{PORT} (GitHub API mode)')
    sys.stdout.flush()
    s.serve_forever()

if __name__ == '__main__':
    main()
