# 🌳 Git Workflow Guide

This document explains the Git branching strategy and workflow used in this project.

## Branch Structure

```
master (main line - production ready)
  ↑
  └─ develop (integration branch)
      ↑
      ├─ feature/selenium-scraper
      ├─ feature/scrapy-spider
      ├─ feature/data-analysis
      └─ bugfix/issue-name (as needed)
```

## Branch Types

### Master Branch
- **Purpose:** Production-ready, stable code
- **Protection:** Should only receive fast-forward merges from develop
- **Tagging:** Release versions tagged here (v1.0.0, etc.)
- **Rule:** Never commit directly; only merge from develop

### Develop Branch
- **Purpose:** Integration branch for features
- **Contains:** Latest development code
- **Stability:** Should be stable and working
- **Rule:** Never commit directly; only merge from feature branches

### Feature Branches
- **Naming:** `feature/<feature-name>`
- **Created from:** develop
- **Merged back to:** develop
- **Examples:**
  - `feature/selenium-scraper`
  - `feature/scrapy-spider`
  - `feature/data-analysis`
  - `feature/error-handling`

### Bugfix Branches
- **Naming:** `bugfix/<issue-name>`
- **Created from:** develop
- **Merged back to:** develop
- **Examples:**
  - `bugfix/duplicate-jobs-issue`
  - `bugfix/timeout-handling`
  - `bugfix/csv-encoding`

### Hotfix Branches (Emergency Fixes)
- **Naming:** `hotfix/<issue-name>`
- **Created from:** master (if critical)
- **Merged back to:** master and develop
- **Used for:** Critical production bugs only

---

## Workflow Steps

### 1. Create a Feature Branch

```bash
# Switch to develop and ensure it's up to date
git checkout develop
git pull origin develop

# Create feature branch
git branch feature/my-feature
git checkout feature/my-feature

# OR create and checkout in one command
git checkout -b feature/my-feature
```

### 2. Make Changes and Commit

```bash
# Make your code changes
# Edit files...

# Stage changes
git add .

# Commit with meaningful message
git commit -m "feat(component): Description of feature"
git commit -m "fix(component): Description of fix"
```

### 3. Push Feature Branch

```bash
# Push to remote (makes it visible on GitHub)
git push origin feature/my-feature

# If pushing for the first time
git push -u origin feature/my-feature
```

### 4. Merge to Develop

```bash
# Switch to develop
git checkout develop

# Merge feature branch
git merge feature/my-feature -m "Merge: Add my feature"

# Push develop to remote
git push origin develop

# Delete local feature branch (optional)
git branch -d feature/my-feature

# Delete remote feature branch
git push origin --delete feature/my-feature
```

### 5. Release to Master (When Ready)

```bash
# Switch to master
git checkout master

# Merge develop
git merge develop -m "Release v1.0.0"

# Tag the release
git tag -a v1.0.0 -m "Version 1.0.0 - Job Scraper Release"

# Push master and tags
git push origin master
git push origin --tags

# Switch back to develop for next cycle
git checkout develop
```

---

## Commit Message Format

Follow this format for clear commit history:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **refactor:** Code restructuring
- **perf:** Performance improvements
- **test:** Test additions/changes
- **chore:** Dependencies, build config
- **ci:** CI/CD changes

### Scope

Component that was changed:
- `selenium`
- `scrapy`
- `analysis`
- `docs`

### Examples

```bash
# Good commit messages
git commit -m "feat(selenium): Add scrolling and job URL extraction"
git commit -m "fix(scrapy): Handle missing job description gracefully"
git commit -m "docs(readme): Update setup instructions"
git commit -m "refactor(pipelines): Simplify data cleaning logic"
git commit -m "chore: Update dependencies to latest versions"

# Less descriptive (avoid)
git commit -m "fix bug"
git commit -m "Update code"
git commit -m "Changes"
```

---

## Workflow Examples

### Example 1: Adding Selenium Feature

```bash
# Create and switch to feature branch
git checkout -b feature/selenium-improvements

# Make changes
# ... edit selenium/job_scraper.py ...
# ... edit selenium/config.py ...

# Stage and commit
git add selenium/
git commit -m "feat(selenium): Add timeout handling for flaky networks

- Increase initial wait from 10 to 15 seconds
- Add retry logic for failed element lookups
- Log timing information for debugging
- Handle StaleElementReference exceptions"

# Push to remote
git push -u origin feature/selenium-improvements

# Switch to develop and merge
git checkout develop
git merge feature/selenium-improvements

# Clean up
git branch -d feature/selenium-improvements
git push origin --delete feature/selenium-improvements
```

### Example 2: Fixing a Bug

```bash
# Create bugfix branch
git checkout -b bugfix/duplicate-removal

# Make fix
# ... edit scrapy_project/pipelines.py ...

# Test the fix
# python scrapy_project/run_spider.py

# Commit
git add scrapy_project/pipelines.py
git commit -m "fix(scrapy): Fix duplicate job detection logic

Duplicate pipeline was comparing exact URL strings which failed
on URLs with query parameters. Now normalizes URLs before comparison.

Fixes #12"

# Push and merge
git push -u origin bugfix/duplicate-removal
git checkout develop
git merge bugfix/duplicate-removal
git push origin develop
git branch -d bugfix/duplicate-removal
```

### Example 3: Emergency Hotfix

```bash
# Create hotfix branch from master
git checkout -b hotfix/critical-bug

# Make and test the fix
# ... fix code ...

# Commit
git commit -m "hotfix: Fix critical CSV encoding issue in export

Jobs with special characters were corrupting the CSV file."

# Merge to master
git checkout master
git merge hotfix/critical-bug
git tag v1.0.1
git push origin master --tags

# Also merge to develop
git checkout develop
git merge hotfix/critical-bug
git push origin develop

# Clean up
git branch -d hotfix/critical-bug
```

---

## Viewing Branch History

```bash
# View all branches
git branch -a

# View branch relationships (graph)
git log --graph --oneline --all

# View commits on current branch
git log --oneline

# View commits not yet on master
git log master..HEAD

# View who changed what
git log -p --follow <file>

# View history in ASCII graph
git log --graph --decorate --oneline --all
```

---

## Undoing Changes

### Undo Last Commit (Not Yet Pushed)

```bash
# Undo last commit, keep changes as staged
git reset --soft HEAD~1

# Undo last commit, keep changes as unstaged
git reset --mixed HEAD~1

# Undo last commit, discard changes (CAREFUL!)
git reset --hard HEAD~1
```

### Undo Unpushed Commits

```bash
# Revert to specific commit
git reset --hard <commit-hash>

# View recent commits to find hash
git reflog
```

### Undo Changes to a File

```bash
# Discard changes to a file
git checkout -- <file>

# OR
git restore <file>
```

---

## Merging Issues

### Dealing with Merge Conflicts

```bash
# During merge, conflicts may occur
git merge feature/my-feature
# CONFLICT (content merge): Merge conflict in file.py

# View conflicted files
git status

# Open and edit the file to resolve
# Look for: <<<<<<< HEAD ... ======= ... >>>>>>>

# After fixing:
git add .
git commit -m "Resolve merge conflicts"
git push origin develop
```

### Preventing Merge Conflicts

```bash
# Before merging, update from develop
git checkout feature/my-feature
git pull origin develop

# Resolve any conflicts locally first
# Then merge cleanly into develop
```

---

## GitHub Integration

### Creating Pull Requests

While this workflow favors command-line, you can also use GitHub PRs:

1. Push feature branch to GitHub
2. GitHub shows "Create Pull Request" button
3. Add description of changes
4. Request review if needed
5. Merge via GitHub UI

---

## Best Practices

✅ **DO:**
- Create feature branches for all work
- Write clear, descriptive commit messages
- Keep feature branches focused and small
- Test before merging
- Keep develop in working condition
- Pull latest before creating branch
- Delete completed branches

❌ **DON'T:**
- Commit directly to master or develop
- Use generic commit messages ("fix", "update")
- Leave unfinished branches hanging
- Force push without discussion
- Merge your own branches to master
- Ignore conflicts
- Commit large binary files

---

## Useful Commands Summary

```bash
# Clone repo
git clone <url>

# Create and switch to feature branch
git checkout -b feature/name

# View status
git status

# Stage changes
git add .

# Commit
git commit -m "message"

# Push branch
git push -u origin feature/name

# View branches
git branch -a

# Switch branches
git checkout develop

# Merge branch
git merge feature/name

# View history
git log --oneline

# Delete local branch
git branch -d feature/name

# Delete remote branch
git push origin --delete feature/name

# View differences
git diff

# Stash changes (temporary)
git stash

# Apply stashed changes
git stash pop
```

---

## Release Checklist

Before releasing to master:

- [ ] All features merged to develop
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Version number updated
- [ ] No known bugs
- [ ] Data/CSV exports working correctly
- [ ] Analysis scripts tested

---

**Remember: This branching model keeps code organized and production-stable!**
