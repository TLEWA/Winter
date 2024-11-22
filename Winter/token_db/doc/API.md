# get /getnumber

Request: NULL
Response: json
```json
{
    "status": 200,
    "number": 10
}
```
status: 
200: Success, 
500: Server error

# get /get/{numbers}

Request: NULL
Response: JSON
```json
{
    "status": 200,
{
    "uid": "123456",
    "token": "52b4e27c-2169-410c-a044-68ea3b388583"
},
... * numbers
}
```
status: 
200: Success, 
401: format error
402: no enough token


# post /change/{uid}

Request: JSON
```json
{
    "cilpboard": "uoaf8yc6",
    "token": "52b4e27c-2169-410c-a044-68ea3b388583"
    // 未获取填 null
}
```
Response: int
200: Success
422: format error
402: cilpboard unavailable


# get /status/{uid}

Request: NULL
Response: JSON
```json
{
    "status": 200,
    "usagerate": 0.712,
    "lasttime": "2020-12-12 12:12:12"
}
```
status: 
200: Success, 
401: format error
402: no uid
usagerate: 使用成功率，由绘图程序上报
lasttime: 上次上报时间

# post /status/{uid}

Request: JSON
```json
{
    "alltimes": 100,
    "usagetimes": 50
}
```
Response: int
200: Success
401: format error
402: no uid

# get /status/list/{number}

Request: NULL
Response: JSON
```json
{
    "status": 200,
    "list": [
        {
            "uid": "123456",
            "usagerate": 0.712,
            "lasttime": "2020-12-12 12:12:12"
        },
        ...
    ]
}

```
status: 
200: Success, 
401: format error
返回使用成功率最低的number个用户

# post /error/{uid}

Request: null
Response: int
200: Success
401: format error
402: no uid

上报某 uid 的 403 