# GIT_INSTRUCTIONS.md
## Flask Security Project — CSRF Attack & Defense

---

## 📁 Branch Structure

```
main_vulnerable  ──────────────────────────────────────────►  (main dev branch)
     │
     ├──► username/feature-name   (your work goes here)
     ├──► username/another-feature
     │
     └── (once all features are merged and app is hardened)
              │
              ▼
           secure                                             (final protected version)
```

| Branch | Purpose |
|---|---|
| `main_vulnerable` | The base working app **with intentional CSRF vulnerabilities**. This is the shared development branch everyone builds on. |
| `secure` | The final version of the app **with CSRF defenses implemented**. Only updated when the team is ready to apply protections. |
| `username/feature-name` | Your personal feature branch. All individual work lives here before being merged into `main_vulnerable`. |

---

## 📏 Collaboration Rules

> These rules keep the project history clean and prevent teammates from overwriting each other's work.

1. **Never commit directly to `main_vulnerable`.**
   All changes go through a feature branch first — no exceptions.

2. **Always branch off `main_vulnerable`.**
   Your feature branch must be created from the latest state of `main_vulnerable`, not from another teammate's branch.

3. **Merge back into `main_vulnerable` via Pull Request (PR) or manual merge.**
   - If using GitHub: open a PR from your branch → `main_vulnerable` and ask a teammate to review.
   - If working locally: use `git merge` (see workflow below).

4. **The `secure` branch is touched last.**
   Only start working on `secure` once `main_vulnerable` is stable and the whole team agrees it's time to implement defenses. Treat `secure` as a final deliverable, not a scratch pad.

---

## 🔄 Recommended Git Workflow (Step-by-Step)

### Step 1 — Get the latest version of `main_vulnerable`

```bash
git checkout main_vulnerable
git pull origin main_vulnerable
```

Always do this before creating a new branch. You want to start from the most up-to-date code.

---

### Step 2 — Create your feature branch

```bash
git checkout -b username/feature-name
```

Replace `username` with your actual Git username and `feature-name` with a short description of what you're building (e.g., `reda/add-login-form`).

---

### Step 3 — Do your work and commit

```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "feat: add login form with CSRF vulnerability demo"
```

**Tips for good commit messages:**
- Use a short prefix: `feat:`, `fix:`, `docs:`, `refactor:`
- Describe *what* and *why*, not *how*
- Keep it under 72 characters

---

### Step 4 — Push your branch to GitHub

```bash
git push origin username/feature-name
```

This uploads your branch so teammates can see it and you can open a PR.

---

### Step 5 — Merge your feature into `main_vulnerable`

#### Option A — Via GitHub Pull Request *(recommended)*
1. Go to the repository on GitHub.
2. Click **"Compare & pull request"** for your branch.
3. Set the base branch to `main_vulnerable`.
4. Add a short description and request a review from a teammate.
5. Once approved, click **"Merge pull request"**.

#### Option B — Manual merge locally
```bash
# Switch to main_vulnerable
git checkout main_vulnerable

# Pull the latest (in case others merged while you were working)
git pull origin main_vulnerable

# Merge your branch in
git merge username/feature-name

# Push the updated main_vulnerable to GitHub
git push origin main_vulnerable
```

---

### Step 6 — Working on the `secure` branch

When the team is ready to implement CSRF defenses:

```bash
# Branch off main_vulnerable (or directly from it if it's the final state)
git checkout main_vulnerable
git pull origin main_vulnerable

git checkout secure
git merge main_vulnerable      # bring in all the latest vulnerable code first

# Now apply your CSRF fixes...
git add .
git commit -m "feat: implement CSRF token protection on all forms"
git push origin secure
```

> 💡 The `secure` branch should be a **mirror of `main_vulnerable`** plus your security patches — not built from scratch.

---

## 🏷️ Branch Naming Conventions

| Pattern | Example |
|---|---|
| `username/feature-name` | `reda/login-csrf-demo` |
| `username/fix-description` | `sara/fix-form-token` |
| `username/docs-topic` | `youssef/update-readme` |

**Rules:**
- Lowercase only
- Use hyphens `-` instead of spaces or underscores
- Keep it short and descriptive (2–4 words max after the `/`)

---

## 🛠️ Quick Git Command Reference

```bash
# See all branches (local + remote)
git branch -a

# Switch to an existing branch
git checkout branch-name

# Create and switch to a new branch
git checkout -b username/feature-name

# Pull latest changes from remote
git pull origin branch-name

# Stage all changes
git add .

# Commit with a message
git commit -m "your message here"

# Push your branch to GitHub
git push origin username/feature-name

# Merge another branch into your current branch
git merge branch-name

# Check current status of your working directory
git status

# View commit history (compact)
git log --oneline --graph
```

---

## 🌿 Visual Branch Flow

```
                        ┌─────────────────────────┐
                        │      main_vulnerable     │  ◄── shared base, always stable
                        └────────────┬────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
   reda/login-form          sara/attack-demo       youssef/docs-update
              │                      │                      │
     (work here)            (work here)             (work here)
              │                      │                      │
              └──────────────────────┴──────────────────────┘
                                     │
                              PR / git merge
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │      main_vulnerable     │  ◄── updated with all features
                        └────────────┬────────────┘
                                     │
                           (team agrees: add defenses)
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │          secure          │  ◄── CSRF protections applied
                        └─────────────────────────┘
```

---

## ⚠️ Common Mistakes to Avoid

- **Don't push directly to `main_vulnerable`** — always go through a feature branch.
- **Don't create your feature branch from `secure`** — always start from `main_vulnerable`.
- **Don't forget to `git pull` before branching** — stale code leads to painful merge conflicts.
- **Don't use vague commit messages** like `"fix"` or `"update"` — future-you will thank present-you.
- **Resolve merge conflicts carefully** — if you're unsure, ask a teammate before forcing a merge.

---

*Last updated by the project team. Any questions? Ask in the group chat before pushing to shared branches.* 🚀