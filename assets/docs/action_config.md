# Actions Configuration

The following are all the available configuration you can use with `with:` when setting up your custom GitHub Actions:

| Name              | Description                                                                                   | Default value                    |
| ----------------- | --------------------------------------------------------------------------------------------- | -------------------------------- |
| `jekyll-repo`     | Jekyll site repo (owner/name). Empty implies current repo.                                    | `""`                             |
| `jekyll-site`     | Path to the Jekyll site                                                                       | `site`                           |
| `vault-dir`       | path to the Obsidian vault                                                                    | `vault`                          |
| `token`           | Token with read-and-write permission for content and PR on `jekyll-repo`                      | `""`                             |
| `args`            | Arguments passed to `main.py`                                                                 | `--force`                        |
| `mode`            | `pr` opens or updates a pull request, `push` pushes to the default branch, `none` syncs only. | `pr`                             |
| `args`            | Arguments passed to `main.py`                                                                 | `--force`                        |
| `branch`          | Branch used in `pr` mode. Fixed names so repeated runs don't create new branches.             | `obsidian-sync`                  |
| `commit-message`  | Custom commit message. `{sha}` is replaced with the short SHA                                 | `chore: sync from vault @ {sha}` |
| `max-deletions`   | Warn above this many deletions. Runs won't fail.                                              | `10`                             |
| `require-date`    | Abort process if a shared noted has no explicit date.                                         | `true`                           |
| `optimise-images` | Compress PNG/JPEG before commiting to save storage.                                           | `false`                          |
| `python-version`  | Python version to run this job.                                                               | `3.13`                           |
