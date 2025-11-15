# 🚀 GitHub Setup Guide

## Quick Upload to GitHub

### Step 1: Create GitHub Repository (2 minutes)

1. Go to [github.com](https://github.com)
2. Click "+" → "New repository"
3. Name it: `audio-watermarking-research` (or your preferred name)
4. Description: "Audio watermarking research with IDEAW, FrEIA, and ensemble learning"
5. Choose: **Public** (for academic sharing) or **Private**
6. **Don't** initialize with README (we already have one)
7. Click "Create repository"

### Step 2: Upload Your Code (3 minutes)

Copy your repository URL from GitHub (looks like: `https://github.com/YOUR_USERNAME/audio-watermarking-research.git`)

Then run these commands in your project directory:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Audio watermarking research platform with IDEAW + FrEIA"

# Add remote (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR_USERNAME/audio-watermarking-research.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Upload (1 minute)

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. Check that README.md displays correctly

---

## What Gets Uploaded

✅ **Included:**
- All source code (backend, frontend)
- Documentation (MD files)
- Specifications (.kiro/specs/)
- Colab notebook template
- Configuration files
- IDEAW and WavMark repositories (cloned)

❌ **Excluded (via .gitignore):**
- Audio files (*.wav, *.mp3) - too large
- Model checkpoints (*.pth, *.pkl) - too large
- Data directories
- Virtual environments
- Node modules
- Build artifacts

---

## For Colab Integration

After uploading to GitHub, you can use this in Colab:

```python
# In your Colab notebook
!git clone https://github.com/YOUR_USERNAME/audio-watermarking-research.git
%cd audio-watermarking-research
```

This makes it easy to:
- Pull latest code changes
- Share code with collaborators
- Version control your research

---

## Updating Code Later

When you make changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Implemented FrEIA-IDEAW training loop"

# Push to GitHub
git push
```

Then in Colab, pull updates:
```python
!git pull origin main
```

---

## Important Notes

### Large Files
- Audio files and model checkpoints are **NOT** uploaded to GitHub (too large)
- Store these in Google Drive instead
- The .gitignore file handles this automatically

### Research Data
- Keep training data in Google Drive
- Keep model checkpoints in Google Drive
- Only code goes to GitHub

### Collaboration
- Share GitHub repo URL with collaborators
- They can clone and contribute
- Use branches for experimental features

---

## Troubleshooting

**"Repository already exists"**
- You may have initialized git before
- Check: `git remote -v`
- If wrong remote: `git remote remove origin` then add correct one

**"Large files rejected"**
- Check .gitignore is working
- Remove large files: `git rm --cached large_file.wav`
- Commit and push again

**"Authentication failed"**
- Use GitHub personal access token instead of password
- Generate at: Settings → Developer settings → Personal access tokens
- Use token as password when pushing

---

## Next Steps After Upload

1. ✅ Verify all files uploaded correctly
2. ✅ Update repository description on GitHub
3. ✅ Add topics/tags: `audio-watermarking`, `deep-learning`, `research`
4. ✅ Star your own repo (optional but fun!)
5. ✅ Share repo URL in your research notes

**Your code is now backed up and ready for Colab! 🎉**
