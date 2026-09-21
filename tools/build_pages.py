"""Build the preserved website for a GitHub Pages project path (stdlib only)."""
import argparse
from pathlib import Path
import re
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
parser.add_argument('--output', type=Path, default=Path('_site'))
parser.add_argument('--base-path', default='')
parser.add_argument('--production', action='store_true', help='Keep indexing enabled; use only at custom-domain cutover.')
args = parser.parse_args()
root, output = args.source.resolve(), args.output.resolve()
base = '/' + args.base_path.strip('/') if args.base_path.strip('/') else ''
if base and not re.fullmatch(r'/[A-Za-z0-9_.-]+', base):
    parser.error('base-path must be a single GitHub repository path')
if output == root or root.is_relative_to(output):
    parser.error('output must not contain the source directory')
if output.exists() and any(output.iterdir()):
    parser.error('output must be empty; use a fresh output directory')
output.mkdir(parents=True, exist_ok=True)

# Only public website files enter the deployment artifact. No archive, tools,
# reports, repository metadata, or custom-domain CNAME is copied.
paths = list(root.glob('*.html'))
for directory in ('uploads', 'files', 'assets'):
    paths.extend(p for p in (root / directory).rglob('*') if p.is_file())
if args.production:
    paths.extend(root / name for name in ('robots.txt', 'sitemap.xml'))
for source in paths:
    destination = output / source.relative_to(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() in ('.html', '.css', '.js'):
        text = source.read_text(encoding='utf-8')
        if base:
            # Preserved HTML/CSS URLs and JS string literals use these roots.
            # Leave JS regular expressions and relative slide JSON paths alone.
            text = re.sub(r'''(["'])(/(?:uploads|assets|files)/)''',
                          lambda m: m[1] + base + m[2], text)
            if source.suffix.lower() == '.html':
                text = re.sub(r'''(\bhref\s*=\s*["'])(/(?!/)[^"']*)(["'])''',
                              lambda m: m[1] + (m[2] if m[2].startswith(base + '/') else base + m[2]) + m[3], text)
        if source.suffix.lower() == '.html' and not args.production:
            text = text.replace('</head>', '<meta name="robots" content="noindex, nofollow"/>\n</head>')
        destination.write_text(text, encoding='utf-8')
    else:
        shutil.copyfile(source, destination)
(output / '.nojekyll').write_text('', encoding='utf-8')
if not args.production:
    (output / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
print(f'Built {len(paths)} website files at {output}; base path: {base or "/"}; production: {args.production}')
