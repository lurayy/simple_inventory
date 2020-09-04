# Back up and download

#### 1. Backup database and mediafiles
- /api/v1/user/backup/create
```
{
    action : backup
}
```
#### Live update of the backup:
- First connect to the web socket
- Use websocket to connect
- 'backup/create/progress/?token='+token
- Test code is named backup_update.html
- After connection, trigger backup/create


#### 2. List of backup (according to date -> time)
- /api/v1/user/backups/get
```
{
    action : get
}
```


#### 3. Download Backed-up database and mediafiles
- /api/v1/user/backup/download
```
{
    action : download,
    date : [date]         <- get form 2
    time : [time]         <- get form 2
}
```

#### 4. Restore [By Selecint db]
- /api/v1/user/backup/restore
```
{
    action : restore,
    method : selection,
    date : 
    time :
}
```