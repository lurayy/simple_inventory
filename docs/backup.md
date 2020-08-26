# Back up and download

#### 1. Backup database and mediafiles
- /api/v1/user/backup/create
```
{
    action : backup
}
```


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
    type : database / mediafiles
}
```

