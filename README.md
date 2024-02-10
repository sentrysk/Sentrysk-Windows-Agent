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

### Users
Get user information from NetUserGetInfo command via win32 net library and returns
```
{
    "username": "",
    "full_name": "",
    "comment": "",
    "flags": "",
    "sid": ""
}
```


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