# Windows System Agent

## Provides
- System Info
- Users Info
- Audit Policies
- Installed Apps
- Services
- Update History
- Missing Updates
- Docker Info
- NPM Info
- Pip Info


## How It Works

### Services
```
wmic service get DisplayName,Name,State,Description /format:csv
```
code runs and returns

```
{
    "DisplayName":"",
    "ServiceName":"",
    "Status":"",
    "Description"
}
```