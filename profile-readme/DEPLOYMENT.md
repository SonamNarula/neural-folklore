# Deployment Instructions

Follow these simple steps to deploy your new flagship engineering profile to GitHub:

## Step 1: Create or open your profile repository
If you haven't already, create a public repository on GitHub with the exact same name as your GitHub username (e.g., `SonamNarula/SonamNarula`). 
> [!NOTE]
> This is a special repository that displays its `README.md` on your main GitHub profile page.

## Step 2: Clone your profile repository
Clone it to your local machine:
```bash
git clone git@github.com:SonamNarula/SonamNarula.git
```

## Step 3: Copy the profile assets
Copy the files from this directory into your profile repository:
- Copy the `README.md` file to the root of your profile repository.
- Copy the `assets/` folder (containing all the custom `.svg` cards) to the root of your profile repository.

The folder structure of your profile repository should look like this:
```
SonamNarula/ (Profile Repository Root)
├── README.md
└── assets/
    ├── contrib-heatmap.svg
    ├── info-card.svg
    ├── projects-card.svg
    ├── roadmap-card.svg
    ├── stack-card.svg
    └── status-card.svg
```

## Step 4: Commit and Push
Commit the changes and push them to your main branch:
```bash
git add README.md assets/
git commit -m "feat: upgrade to flagship engineering profile v2.0"
git push origin main
```

## Step 5: Verify
Visit your GitHub profile page (`https://github.com/SonamNarula`) and enjoy your high-fidelity, unified Tokyo Night terminal-style dashboard!
