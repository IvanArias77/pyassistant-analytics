# =====================================================
# PyAssistant Analytics - Automated Deploy to Railway
# Built for Ivan Arias
# Usage: powershell -ExecutionPolicy Bypass -File deploy_to_railway.ps1
# =====================================================

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Colors
function Write-Step($msg) { Write-Host "`n[$([DateTime]::Now.ToString('HH:mm:ss'))] $msg" -ForegroundColor Cyan }
function Write-OK($msg) { Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "  [WARN] $msg" -ForegroundColor Yellow }
function Write-Fail($msg) { Write-Host "  [FAIL] $msg" -ForegroundColor Red }
function Write-Info($msg) { Write-Host "  [INFO] $msg" -ForegroundColor Gray }

# =====================================================
# STEP 1: Verify environment
# =====================================================
Write-Step "STEP 1/10: Verifying environment"

# Check git
try {
    $gitVersion = git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-OK "Git installed: $gitVersion"
    }
} catch {
    Write-Fail "Git not installed. Install from: https://git-scm.com/downloads"
    exit 1
}

# Check we're in the right directory
$expectedFiles = @("Dockerfile", "README.md", "backend", "frontend")
$missing = @()
foreach ($f in $expectedFiles) {
    if (-not (Test-Path $f)) {
        $missing += $f
    }
}
if ($missing.Count -gt 0) {
    Write-Fail "Missing files: $($missing -join ', ')"
    Write-Info "Run this script from the pyassistant-analytics root directory"
    exit 1
}
Write-OK "All project files present"

# =====================================================
# STEP 2: Check Python (optional)
# =====================================================
Write-Step "STEP 2/10: Checking Python (optional)"

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-OK "Python found: $pythonVersion"
    }
} catch {
    Write-Warn "Python not in PATH (not blocking deploy)"
}

# =====================================================
# STEP 3: Verify .env is NOT tracked
# =====================================================
Write-Step "STEP 3/10: Verifying .env is not tracked"

$gitignoreContent = Get-Content ".gitignore" -Raw -ErrorAction SilentlyContinue
if ($gitignoreContent -match "\.env") {
    Write-OK ".env is in .gitignore"
} else {
    Write-Fail ".env NOT in .gitignore!"
    exit 1
}

# =====================================================
# STEP 4: Initialize git
# =====================================================
Write-Step "STEP 4/10: Initializing git repository"

if (Test-Path ".git") {
    Write-OK "Git already initialized"
} else {
    git init
    if ($LASTEXITCODE -eq 0) {
        Write-OK "Git initialized"
    } else {
        Write-Fail "Failed to initialize git"
        exit 1
    }
}

# Set git user if not set
$userName = git config user.name 2>&1
$userEmail = git config user.email 2>&1
if ([string]::IsNullOrWhiteSpace($userName)) {
    Write-Warn "Git user.name not configured"
    $name = Read-Host "Enter your git name (e.g., Ivan Arias)"
    git config user.name "$name"
    Write-OK "Set user.name to: $name"
}
if ([string]::IsNullOrWhiteSpace($userEmail)) {
    Write-Warn "Git user.email not configured"
    $email = Read-Host "Enter your git email (e.g., ivan.ariasg@hotmail.com)"
    git config user.email "$email"
    Write-OK "Set user.email to: $email"
}

# =====================================================
# STEP 5: Stage and commit
# =====================================================
Write-Step "STEP 5/10: Staging and committing files"

$gitStatus = git status --porcelain
if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-OK "No changes to commit (already clean)"
} else {
    Write-Info "Files to commit:"
    git status --short

    git add .
    if ($LASTEXITCODE -eq 0) {
        Write-OK "Files staged"
    } else {
        Write-Fail "Failed to stage files"
        exit 1
    }

    git commit -m "Deploy: PyAssistant Analytics v1.0

Full-stack AI productivity dashboard with FastAPI + Gemini"
    if ($LASTEXITCODE -eq 0) {
        Write-OK "Commit created"
    } else {
        Write-Warn "Commit may have failed (no changes?)"
    }
}

# =====================================================
# STEP 6: GitHub repo setup
# =====================================================
Write-Step "STEP 6/10: GitHub repository setup"

$remoteUrl = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($remoteUrl)) {
    Write-OK "GitHub remote already configured: $remoteUrl"
} else {
    Write-Info "Create the GitHub repo first (cannot be done via CLI without auth):"
    Write-Info ""
    Write-Info "1. Open: https://github.com/new"
    Write-Info "2. Repository name: pyassistant-analytics"
    Write-Info "3. Description: Personal AI-powered productivity dashboard"
    Write-Info "4. Visibility: PUBLIC (for recruiters)"
    Write-Info "5. DO NOT initialize with README (we have one)"
    Write-Info "6. Click 'Create repository'"
    Write-Info ""
    $repoUrl = Read-Host "Paste the repo URL (e.g., https://github.com/IvanArias77/pyassistant-analytics.git)"

    if ([string]::IsNullOrWhiteSpace($repoUrl)) {
        Write-Fail "No URL provided"
        exit 1
    }

    git remote add origin $repoUrl
    if ($LASTEXITCODE -eq 0) {
        Write-OK "Remote added: $repoUrl"
    } else {
        Write-Fail "Failed to add remote"
        exit 1
    }
}

# =====================================================
# STEP 7: Push to GitHub
# =====================================================
Write-Step "STEP 7/10: Pushing to GitHub"

$currentBranch = git branch --show-current 2>&1
if ($currentBranch -ne "main") {
    git branch -M main 2>&1 | Out-Null
    Write-OK "Branch renamed to main"
}

Write-Info "Pushing to origin/main..."
git push -u origin main
if ($LASTEXITCODE -eq 0) {
    Write-OK "Code pushed to GitHub!"
} else {
    Write-Fail "Failed to push. Check your GitHub credentials."
    Write-Info "If using HTTPS, you may need a Personal Access Token:"
    Write-Info "https://github.com/settings/tokens"
    exit 1
}

# =====================================================
# STEP 8: Railway deploy instructions
# =====================================================
Write-Step "STEP 8/10: Railway deploy setup"

Write-Info "Now deploy on Railway:"
Write-Info ""
Write-Info "1. Open: https://railway.app/new"
Write-Info "2. Click 'Deploy from GitHub repo'"
Write-Info "3. Select: IvanArias77/pyassistant-analytics"
Write-Info "4. Railway will detect the Dockerfile and start building"
Write-Info ""
Write-Info "While building, go to Variables tab and add:"
Write-Info "  GEMINI_API_KEY=AIza... (your Gemini key, optional)"
Write-Info "  DEBUG=False"
Write-Info "  SECRET_KEY=random-32-chars-string"
Write-Info ""
Read-Host "Press Enter when Railway is deploying (or Ctrl+C to stop here)" | Out-Null

# =====================================================
# STEP 9: Get public URL
# =====================================================
Write-Step "STEP 9/10: Getting your public URL"

Write-Info "Once deploy is complete (green check):"
Write-Info ""
Write-Info "1. In Railway, go to Settings -> Domains"
Write-Info "2. Click 'Generate Domain'"
Write-Info "3. Copy the URL (e.g., https://pyassistant-analytics-production.up.railway.app)"
Write-Info ""
$appUrl = Read-Host "Paste your Railway URL here (or press Enter to skip)"

if (-not [string]::IsNullOrWhiteSpace($appUrl)) {
    Write-OK "URL saved: $appUrl"
    $appUrl | Out-File -FilePath ".\APP_URL.txt" -Encoding UTF8
    Write-OK "URL saved to APP_URL.txt"
}

# =====================================================
# STEP 10: Post-deploy verification
# =====================================================
Write-Step "STEP 10/10: Verifying deploy"

if (-not [string]::IsNullOrWhiteSpace($appUrl)) {
    Write-Info "Testing endpoints..."

    try {
        $healthResponse = Invoke-WebRequest -Uri "$appUrl/api/health" -UseBasicParsing -TimeoutSec 30
        if ($healthResponse.StatusCode -eq 200) {
            Write-OK "Health check: 200 OK"
        }
    } catch {
        Write-Warn "Could not reach health endpoint (normal if just deployed)"
    }

    try {
        $docsResponse = Invoke-WebRequest -Uri "$appUrl/docs" -UseBasicParsing -TimeoutSec 30
        if ($docsResponse.StatusCode -eq 200) {
            Write-OK "API docs: 200 OK (Swagger UI available)"
        }
    } catch {
        Write-Warn "API docs not reachable yet"
    }
} else {
    Write-Info "Skipped verification (no URL provided)"
}

# =====================================================
# Final summary
# =====================================================
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "  DEPLOY PROCESS COMPLETE!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host ""

if (-not [string]::IsNullOrWhiteSpace($appUrl)) {
    Write-Host "  Your app is live at:" -ForegroundColor Cyan
    Write-Host "  $appUrl" -ForegroundColor White -BackgroundColor DarkBlue
    Write-Host ""
    Write-Host "  Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Open your URL in a browser to verify the dashboard"
    Write-Host "  2. Railway Settings -> Volumes -> Add Volume (/app/data)"
    Write-Host "  3. Railway Shell: python -m data.seed"
    Write-Host "  4. Update CV and LinkedIn with the URL"
    Write-Host "  5. Apply to jobs using your URL as portfolio"
} else {
    Write-Host "  Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Complete Railway setup manually"
    Write-Host "  2. Run this script again to verify"
    Write-Host "  3. Or follow Ivan_Arias_Deploy_Guide_Railway.docx"
}

Write-Host ""
Read-Host "Press Enter to exit" | Out-Null
