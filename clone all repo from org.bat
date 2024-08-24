# Define as variáveis
$token = "your-github-token"
$orgName = "your-org-name"
$baseDir = "your-base-dir"

# Cria a pasta base se não existir
if (-not (Test-Path $baseDir)) {
    New-Item -ItemType Directory -Path $baseDir
}

# Obtém todos os repositórios da organização
$repos = Invoke-RestMethod -Uri "https://api.github.com/orgs/$orgName/repos?per_page=200" -Headers @{Authorization = "token $token"}

# Clona cada repositório
foreach ($repo in $repos) {
    $repoName = $repo.name
    $repoUrl = $repo.clone_url
    $targetDir = Join-Path $baseDir $repoName

    if (-not (Test-Path $targetDir)) {
        Write-Host "Cloning $repoName into $targetDir"
        git clone $repoUrl $targetDir
    } else {
        Write-Host "$repoName already exists in $targetDir, pulling latest changes"
        cd $targetDir
        git pull
        cd $baseDir
    }
}
