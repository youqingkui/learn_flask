# Learn Python Flask

[toc]

## 安装Flask
一般使用第三方实用工具virtualenv创建虚拟环境
```sh
# 安装virtualenv
sudo easy_install virtualenv`
# 创建虚拟
virtualenv venv
# 安装flask
pip install flask
```

## 程序基本结构

### app = Flask(\__name__)
Flask用这个参数决定程序的根目录，以便稍后能够找到相对于程序根目录的资源文件位置。
```py
from flask import Flask
app = Flask(__name__)
```


### 请求钩子

`before_first_request`：注册一个函数，在处理第一个请求之前运行。
`before_request`：注册一个函数，在每次请求之前运行。
`after_request`：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。(暂不明白)
`teardown_request`：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行（暂不明白）


>通常使用`before_request`来验证用户是否登陆，没有检查到session，则让用户跳转。

### `abort` 处理
可以快速返回http状态错误，并且不执行后面代码

```py
from flask import abort

@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name
```

### return http状态

可以在return后面跟http状态
```py
@app.route('/')
def index():
    return '<h1>Bad Request</h1>', 400
```


### `make_response` 返回请求，并且设置cookie
可以使用`make_response` 包含一些文本，但是感觉与return  后面加内容差不多。只是可以说设置返回的cookie

```py
from flask import make_response

@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
```

### 使用Flask-Scrip
使用此扩展可以方便的启动shell管理，要运行服务器的时候，需要python app.py runserver  后面可以跟一些选项 `-d ` 开启DEBUG， `-r` 修改代码自动重新载入重启。




>  这个很有用，什么上下文之类的， 也有些不太理解
>```sh
>>> from hello import app
>>> from flask import current_app
>>> current_app.name
Traceback (most recent call last):
...
RuntimeError: working outside of application context
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> current_app.name
'hello'
>>> app_ctx.pop()
>```
在这个例子中，没激活程序上下文之前就调用current_app.name会导致错误，但推送完上下文之后就可以调用了。注意，在程序实例上调用app.app_context()可获得一个程序上下文。


## 模板

### 宏

为了重复使用宏，我们可以将其保存在单独的文件中，然后在需要使用的模板中导入

```html
{# form表单宏定义 form.html #}

{% macro input(labeltext, name, col, value='', type='text', isneed=False, errormsg='') -%}
<div class="form-group">
    <label class="control-label col-md-1">{{ labeltext }}</label>
    <div class="{{ col }}">
        <input class="form-control" type="{{ type }}" name="{{ name }}" id="{{ name }}" value="{{ value }}">
        {% if isneed %}<span style="color: #ff4500">*</span>{% endif %}
        {% if errormsg %}<span class="label label-important">{{ errormsg }}</span>{% endif %}
    </div>
</div>
{%- endmacro %}

```
> 在其他的页面可以直接使用导入
> ```html
> {% import 'form.html' as form %}
> {{form.input('Host', 'host', 'col-md-4', 'localhost')}}
> ```



### 自定义错误页面
和视图函数一样，错误处理程序也会返回响应。它们还返回与该错误对应的数字状态码
```py
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```


### `url_for()` 生成链接
在蓝图中可以使用对应的视图函数， `url_for('care.find')` 将会对应下面代码路由
```py
@care.route('/find')
def find():
	pass
```
也可以使用生成静态文件的链接

```py
# http://localhost:5000/static/css/styles.css
url_for('static', filename='css/styles.css', _external=True)
```



