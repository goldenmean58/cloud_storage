# 用户部分

## 注册

`method`: `POST`

`path`: `/user/register`

`args`:

`username`: 用户名

`password`: 密码

`return valule`:

```json
{
	'code': 0,
	'msg': 'Register successfully'
}
```

## 登录

`method`: `POST`

`path`: `/user/login`

`args`:

`username`: 用户名

`password`: 密码

`return valule`:

```json
{
	'code': 0,
	'msg': 'Login successfully'
}
```

## 登出

`method`: `POST`

`path`: `/user/logout`

`return valule`:

```json
{
	'code': 0,
	'msg': 'Logout successfully'
}
```

# 文件部分

## 查看

`method`: `POST`

`path`: `/files/view`

`args`:

`path`: 绝对路径(根目录/)，可以是文件或文件夹

`user`: 用户名

`key`: 分享码(可选)

## 建立文件夹

`method`: `POST`

`path`: `/files/create_dir`

`args`:

`current_dir`: 当前文件夹的绝对路径(根目录/)

`dir_name`: 要创建的文件夹名


## 上传文件

`method`: `POST`

`path`: `/files/upload`

`args`:

`current_dir`: 当前文件夹的绝对路径(根目录/)

`file`: 文件

## 下载文件

`method`: `POST`

`path`: `/files/get_download`

`args`:

`user`: 用户名

`path`: 文件的绝对路径

`key`: 分享码(可选)

`return value`:

```json
{
	'code': 0,
	'link': xxx
}
```

`method`: `GET`

`path`: `/files/download/xxx/` xxx为上面获得的`link`,下载链接有有效期,过期需要重新获取

## 删除文件/文件夹

`method`: `POST`

`path`: `/files/delete`

`args`:

`current_dir`: 当前所在文件夹路径

`file_name`: 要删除的文件或文件夹名

## 移动文件/文件夹

`method`: `POST`

`path`: `/files/move`

`args`:

`src_path`: 源绝对路径

`dest_path`: 目的绝对路径

## 复制文件/文件夹

`method`: `POST`

`path`: `/files/copy`

`args`:

`src_path`: 源绝对路径

`dest_path`: 目的绝对路径

## 分享

`method`: `POST`

`path`: `/files/share`

`args`:

`current_dir`: 当前所在文件夹的绝对路径

`file_name`: 要分享的文件/文件夹名

`key`: 分享码

`day`: 分享过期天数

## 取消分享

`method`: `POST`

`path`: `/files/unshare`

`args`:

`current_dir`: 当前所在文件夹的绝对路径

`file_name`: 文件/文件夹名
