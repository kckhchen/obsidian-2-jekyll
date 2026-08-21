# Actions Configuration

## Available Config

The following are all the available configuration you can use with `with:` when setting up your custom GitHub Actions:

| Name              | Description                                                                                   | Default value                    |
| ----------------- | --------------------------------------------------------------------------------------------- | -------------------------------- |
| `jekyll-repo`     | Jekyll site repo (owner/name). Must differ from your vault repo.                              | `""`                             |
| `jekyll-dir`      | Path to the Jekyll site                                                                       | `site`                           |
| `vault-dir`       | path to the Obsidian vault                                                                    | `vault`                          |
| `token`           | Token with read-and-write permission for content and PR on `jekyll-repo`                      | `""`                             |
| `args`            | Arguments passed to `main.py`                                                                 | `--force`                        |
| `mode`            | `pr` opens or updates a pull request, `push` pushes to the default branch, `none` syncs only. | `pr`                             |
| `branch`          | Branch used in `pr` mode. Fixed names so repeated runs don't create new branches.             | `obsidian-sync`                  |
| `commit-message`  | Custom commit message. `{sha}` is replaced with the short SHA                                 | `chore: sync from vault @ {sha}` |
| `max-deletions`   | Warn above this many deletions. Runs won't fail.                                              | `10`                             |
| `require-date`    | Abort process if a shared noted has no explicit date.                                         | `true`                           |
| `optimise-images` | Compress PNG/JPEG before commiting to save storage.                                           | `false`                          |
| `python-version`  | Python version to run this job.                                                               | `3.13`                           |

## Outputs

| Name               | Description                                |
| ------------------ | ------------------------------------------ |
| `changed`          | `true` when the sync produced a change.    |
| `deletions`        | Number of files the sync would delete.     |
| `posts-written`    | Number of post files after the sync.       |
| `pull-request-url` | URL of the pull request opened or updated. |

```yaml
- uses: kckhchen/obsidian-2-jekyll@v0
  id: sync
  with:
    jekyll-repo: username/jekyll-repo
    token: ${{ secrets.BLOG_PUSH_TOKEN }}
    args: --update --force --yes

- if: steps.sync.outputs.deletions > 0
  run: echo "::notice::${{ steps.sync.outputs.pull-request-url }} deletes ${{ steps.sync.outputs.deletions }} file(s)"
```
