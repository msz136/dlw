"""Archive old Git metadata and rebuild reachable refs without the large snapshot.

No files or Git objects are deleted. The complete original repository remains
recoverable inside Trash, including its snapshot branch and reflogs.
"""
from pathlib import Path
from datetime import datetime
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SNAPSHOT = 'refs/heads/codex/local-full-snapshot-20260930'


def git(*args, git_dir=None):
    prefix = ['git'] if git_dir is None else ['git', '--git-dir=' + str(git_dir)]
    return subprocess.check_output(prefix + list(args), cwd=ROOT).decode('utf-8')


def size(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())


def check_move(source, target):
    source = source.resolve()
    target = target.resolve()
    assert source.is_relative_to(ROOT) and target.is_relative_to(ROOT)
    assert source != ROOT and target != ROOT and not target.exists()
    return source, target


def move(source, target):
    source, target = check_move(source, target)
    # Force handles the Windows hidden attribute on the original .git folder.
    quote = lambda p: "'" + str(p).replace("'", "''") + "'"
    command = f'Move-Item -LiteralPath {quote(source)} -Destination {quote(target)} -Force -ErrorAction Stop'
    subprocess.run(['powershell', '-NoProfile', '-Command', command], check=True)


def main():
    old = ROOT / '.git'
    assert old.is_dir()
    assert git('branch', '--show-current').strip() == 'main'
    assert git('worktree', 'list', '--porcelain').count('worktree ') == 1
    assert not git('diff', '--cached', '--name-only').strip()
    head = git('rev-parse', 'HEAD').strip()
    remote = git('ls-remote', 'origin', 'refs/heads/main').split()[0]
    assert head == remote, 'Finish pushing current results before archiving.'
    refs = {}
    for line in git('for-each-ref', '--format=%(refname) %(objectname)').splitlines():
        ref, oid = line.split()
        refs[ref] = oid
    assert SNAPSHOT in refs
    tracked = git('ls-files', '-z')
    status = git('status', '--porcelain=v1', '--untracked-files=no')
    stashes = git('stash', 'list')
    stash_oids = git('reflog', 'show', '--format=%H', 'refs/stash').splitlines()
    symrefs = {}
    for line in git('for-each-ref', '--format=%(refname) %(symref)').splitlines():
        parts = line.split()
        if len(parts) == 2:
            symrefs[parts[0]] = parts[1]
    temp = HERE / ('compact_' + datetime.now().strftime('%H%M%S') + '.git')
    assert not temp.exists()
    subprocess.run(['git', 'init', '--bare', '--initial-branch=main', str(temp)], check=True, capture_output=True)
    specs = [f'{ref}:{ref}' for ref in refs if ref != SNAPSHOT and ref not in symrefs]
    specs += [f'{oid}:refs/preserved-stashes/{i:02d}' for i, oid in enumerate(stash_oids)]
    subprocess.run(['git', '--git-dir=' + str(temp), 'fetch', '--no-tags', '--no-write-fetch-head', str(ROOT), *specs], check=True)
    for ref, target in symrefs.items():
        git('symbolic-ref', ref, target, git_dir=temp)
    # Restore the original non-bare configuration and ancillary local settings.
    shutil.copy2(old / 'config', temp / 'config')
    for name in ('info/exclude', 'info/attributes', 'logs/refs/stash'):
        source = old / name
        if source.is_file():
            destination = temp / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    assert git('rev-parse', 'HEAD', git_dir=temp).strip() == head
    assert not git('for-each-ref', '--format=%(refname)', SNAPSHOT, git_dir=temp).strip()
    for ref, oid in refs.items():
        if ref != SNAPSHOT:
            assert git('rev-parse', ref, git_dir=temp).strip() == oid
    old_bytes = size(old)
    new_bytes = size(temp)
    assert new_bytes < old_bytes
    archive = ROOT / 'Trash' / ('git_snapshot_20261010_' + datetime.now().strftime('%H%M%S'))
    assert archive.resolve().is_relative_to((ROOT / 'Trash').resolve())
    archive.mkdir(parents=True, exist_ok=False)
    old_source, archive_target = check_move(old, archive / '.git')
    move(old_source, archive_target)
    try:
        source, target = check_move(temp, old)
        move(source, target)
        git('reset', '--mixed', 'HEAD')
        assert git('ls-files', '-z') == tracked
        assert git('status', '--porcelain=v1', '--untracked-files=no') == status
        assert git('stash', 'list') == stashes
        assert git('rev-parse', 'HEAD').strip() == head
        assert git('rev-parse', SNAPSHOT, git_dir=archive / '.git').strip() == refs[SNAPSHOT]
    except Exception:
        if old.exists():
            source, target = check_move(old, archive / 'failed_compact.git')
            move(source, target)
        source, target = check_move(archive / '.git', old)
        move(source, target)
        raise
    result = {
        'date': '2026-10-10', 'pushed_commit_before_archive': head,
        'archived_snapshot': SNAPSHOT, 'snapshot_commit': refs[SNAPSHOT],
        'original_git_archive': str(archive / '.git'),
        'original_git_bytes': old_bytes, 'new_git_bytes': size(old),
        'retained_refs': {ref: oid for ref, oid in refs.items() if ref != SNAPSHOT},
        'stashes_preserved': len(stash_oids),
        'tracked_file_list_and_worktree_changes_unchanged': True,
        'deletions': 0,
    }
    (HERE / 'archive_result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (archive / 'README.txt').write_text(
        'Complete original Git metadata, preserved without deleting objects.\n'
        f'Snapshot: {SNAPSHOT} {refs[SNAPSHOT]}\n'
        'Inspect with git --git-dir=<this-directory>/.git log --all.\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
