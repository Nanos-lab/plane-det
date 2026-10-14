# 初始化与验证脚本
# 固定使用 conda 环境 imgforge 的 Python，不走 conda run / conda activate

$PythonExe = "E:\anaconda3\envs\imgforge\python.exe"

Write-Host "=== 初始化检查开始 ==="

if (-not (Test-Path $PythonExe)) {
    Write-Error "找不到 Python 解释器: $PythonExe"
    exit 1
}

& $PythonExe --version

if (Test-Path "requirements.txt") {
    Write-Host "=== 安装依赖 (requirements.txt) ==="
    & $PythonExe -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

if (Test-Path "tests") {
    Write-Host "=== 运行测试 (pytest) ==="
    & $PythonExe -m pytest
    if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 5) { exit $LASTEXITCODE }
} else {
    Write-Host "未发现 tests 目录，跳过测试"
}

Write-Host "=== 初始化检查完成 ==="