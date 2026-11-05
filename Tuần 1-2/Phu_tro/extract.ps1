$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $dir) { $dir = (Get-Location).Path }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $file = Get-ChildItem -LiteralPath $dir -Filter "*final.doc" | Select-Object -First 1
    Write-Host "Found file: $($file.FullName)"
    $doc = $word.Documents.Open($file.FullName, $false, $true)
    $text = $doc.Content.Text
    $outTxt = Join-Path $dir "de_cuong_extracted.txt"
    [System.IO.File]::WriteAllText($outTxt, $text, [System.Text.Encoding]::UTF8)
    $outDocx = Join-Path $dir "de_cuong_converted.docx"
    $doc.SaveAs2($outDocx, 16)
    Write-Host "Extracted text and converted docx successfully!"
} catch {
    Write-Error $_
} finally {
    if ($doc) { $doc.Close([ref]0) }
    $word.Quit()
}
