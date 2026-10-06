$ErrorActionPreference = 'Stop'
& 'C:\Users\msz\aca\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs' `
  -File 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs\ReportEndpoints.lean' `
  -TimeoutSeconds 300
exit $LASTEXITCODE
