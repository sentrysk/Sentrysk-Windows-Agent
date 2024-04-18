# Sentrysk Windows Agent

| Content  | 
| ------------- |
| [Project Architecture](##Architecture)     | 
| [Requirements](https://github.com/sentrysk/Sentrysk-Windows-Agent/blob/main/README.md#requirements) |
| [How to Install](https://github.com/sentrysk/Sentrysk-Windows-Agent/blob/main/README.md#how-to-install)   | 
| [Roadmap](https://github.com/sentrysk/Sentrysk-Windows-Agent/blob/main/README.md#roadmap)   | 
| [How it Works](https://github.com/sentrysk/Sentrysk-Windows-Agent/blob/main/README.md#how-it-works)    | 

## Architecture

## Requirements
| Program  | Version |
| ------------- |:-------------:|
| Python      | 3.10     |

## How To Install

- Install requirements
**Using admin rights** 
```
pip install -r requirements.txt
```

## Roadmap
### Version 1.0-Beta
- [x] [Developing NPM data collector module](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/1)
- [x] [Developing Pip data collector module](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/2)
- [x] [Developing installed apps data collector module](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/3)
- [x] [Developing last logons data collector module](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/4)
- [x] [Developing services data collector module](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/5)
- [x] [Developing users data collector module](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/6)
- [x] [Developing system information data collector module](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/7)
- [x] [Developing docker data collector module](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/8)
- [x] [Developing config file](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/9)
- [x] [Developing data sender functions](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/10)
- [x] [Developing scheduled jobs](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/11)
- [ ] [Developing config sender module](https://github.com/sentrysk/Sentrysk-Windows-Agent/issues/12)

### Feature Development
- [ ] Process data collector module
- [ ] Memory data collector module (planning to keep 1 month data)
- [ ] CPU data collector module (planning to keep 1 month data)



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
