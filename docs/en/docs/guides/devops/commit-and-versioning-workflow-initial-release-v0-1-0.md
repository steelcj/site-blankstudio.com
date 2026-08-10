# Initial release and publish

## Initial Release

```bash
nano VERSION
```

Content

```bash
0.0.0
```

Then initial commit is the VERSION file

```bash
git add VERSION 
git commit -m 'VERSION'
```

Then

```bash
python3 cut-release.py 0.1.0
```

then

```bash
git push && git push origin v0.1.0
```

output example:

```bash
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 8 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (7/7), 1.52 KiB | 1.52 MiB/s, done.
Total 7 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:steelcj/site-blankstudio.com.git
 * [new branch]      main -> main
Enumerating objects: 1, done.
Counting objects: 100% (1/1), done.
Writing objects: 100% (1/1), 170 bytes | 170.00 KiB/s, done.
Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:steelcj/site-blankstudio.com.git
 * [new tag]         v0.1.0 -> v0.1.0
```

## Initial publish-release

```bash
python3 publish-release.py
```

Output example:

```bash
python3 publish-release.py 
[publish-release] backend: gh, tag v0.1.0 verified locally and on origin
[publish-release] built: site-blankstudio.com-0.1.0.tar.gz (1346 bytes, sha256 d6639d9b49e30426…, deterministic)
[publish-release] gpg or a secret key is unavailable; publishing unsigned (allowed, never blocking).

[publish-release] published v0.1.0 via gh:
  https://github.com/steelcj/site-blankstudio.com/releases/tag/v0.1.0

```

