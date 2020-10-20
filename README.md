# Scrapy

scrapyを使ってwebページの情報を取得し、最終的にMySQLとjsonファイルに登録したいと思います。

## install

```console
pip install scrapy
```

## start project

```console
scrapy startproject <プロジェクト名>
```

## create spider

```console
scrapy genspider <ファイル名> <スクレイピングしたいweb URL>
```

## running

```console
scrapy crawl <クロール名> -o <出力するファイル名 csv or json>
```

今回の場合は...

```console
scrapy crawl magazine -o magazine.json
```


## MySQL

```sql
create database scrapy;
create table scrapy.magazine (
  `guid` varchar(32) not null primary key,
  `title` text null,
  `url` text null,
  `created` datetime default CURRENT_TIMESTAMP not null,
  `updated` datetime default CURRENT_TIMESTAMP not null
);
```

## config

```pipelines.py```と同階層に```db_connect.py```を配置してください。

```python:db_connect.py
db_connect = {
  'DB_HOST'    : 'ホスト名',
  'DB'         : 'データベース名',
  'DB_USER'    : 'ユーザー名',
  'DB_PASSWORD': 'パスワード',
}
```

・参考: [https://www.wantedly.com](https://www.wantedly.com/companies/roxx/post_articles/137315)
