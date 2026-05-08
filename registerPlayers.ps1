$server = "http://localhost:5000/api/players"

$players = @(
  @{ id="a9cd1ada-c81a-463a-b997-b6ef8ee57da9"; name="Random Boss"; address="http://localhost:9080" }
   @{ id="a9cd1ada-c81a-463a-b997-b6ef8ee57da8"; name="Basic AI"; address="http://localhost:9082" }

)

foreach ($p in $players) {
  Invoke-WebRequest `
    -Method Post `
    -Uri $server `
    -Headers @{ 'Content-Type' = 'application/json' } `
    -Body ($p | ConvertTo-Json -Compress) |
    Out-Null
}

"Players registered."