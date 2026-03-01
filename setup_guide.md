# Setup Guide: Blogger-to-GitHub Video Fingerprinting

Follow these steps to get your automated video fingerprint modification system running on your Blogger site.

## 1. Push Code to GitHub

Ensure all files in your local `video_fingerprint` directory are pushed to your GitHub repository, including:

- `modify_fingerprint.py`
- `.github/workflows/modify_fingerprint_action.yml` (Critical for the backend)

## 2. Generate a GitHub Token (PAT)

Your Blogger UI needs permission to talk to GitHub.

1. Go to **GitHub Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**.
2. Click **Generate new token (classic)**.
3. Name it (e.g., "Blogger Video Tool").
4. Select the following scopes:
    - [x] **repo** (Full control of private repositories)
    - [x] **workflow** (Update GitHub Action workflows)
5. **Copy the token immediately** (It will look like `ghp_xxxxxxxxxxxx`).

## 3. Setup Blogger Frontend (Choose Method A or B)

### Method A: Single Page (Recommended if you have an existing blog)

1. Log in to your **Blogger Dashboard**.
2. Create a new **Post** or **Page**.
3. Switch the editor to **HTML View** (click the pencil/brackets icon).
4. Open [blogger_ui.html](file:///c:/Users/Argha/Downloads/video_fingerprint/blogger_ui.html) and copy its entire content.
5. Paste it into the Blogger HTML editor and **Publish**.

### Method B: Full Blog Theme (Hidden Admin UI)

1. Log in to your **Blogger Dashboard**.
2. Go to **Theme** > click the arrow next to **Customize** > select **Edit HTML**.
3. Open [blogger_theme.xml](file:///c:/Users/Argha/Downloads/video_fingerprint/blogger_theme.xml).
4. **Edit the Configuration**: Scroll down to line ~260-265 and fill in your details:

    ```javascript
    const GITHUB_USER = 'apka-username';
    const GITHUB_REPO = 'video_fingerprint';
    const GITHUB_TOKEN = 'ghp_apka_token_yahan';
    ```

5. Select all existing code in the Blogger HTML editor, delete it, and paste your **edited** code.
6. Click **Save**.

## 4. How to Use

1. Open your published Blogger page.
2. Enter your **GitHub Username**, **Repo Name**, and the **Token (PAT)** you generated.
3. Paste a **YouTube URL**.
4. Click **Modify Fingerprint**.
5. Wait for the progress dots to turn green (2-5 mins).
6. Click the **Download Modified Video** button that appears.

> [!TIP]
> **Browser Storage**: Once you enter your GitHub details, your browser may remember them for next time, so you won't have to type them every time you use the tool on that computer.
