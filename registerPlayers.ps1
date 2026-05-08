$server = "http://localhost:5000/api/players"

$players = @(
  @{ id="a9cd1ada-c81a-463a-b997-b6ef8ee57da9"; name="Giant Wipeout"; address="http://localhost:9080" }
  @{ id="7c3c1128-792c-46b2-afa1-1de3e55974e2"; name="Purple spawn";  address="http://localhost:9080" }
  @{ id="cc9ddc91-2e0d-4565-af30-a39748f2344b"; name="Swamp prawns";   address="http://localhost:9080" }
  @{ id="d9db5f7c-7f30-4c13-a4d5-9f6a8b9b2c1d"; name="Fourth team";   address="http://localhost:9080" }
    @{ id="d9db5f7c-7f30-4c13-a4d5-9f6a8b9b2c4d"; name="5 team";   address="http://localhost:9080" }
	  @{ id="d9db5f7c-7f30-4c13-a4d5-9f6a8b9b2c6d"; name="6 team";   address="http://localhost:9080" }
	      @{ id="d9db5f7c-7f30-4c13-a4d5-9f6a8b9b2f4d"; name="7 team";   address="http://localhost:9080" }
	  @{ id="d9db5f7c-7f30-4c13-a4d5-9f6a8b9b2c7d"; name="8 team";   address="http://localhost:9080" }
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