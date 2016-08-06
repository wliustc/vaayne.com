## 关于
Vaayne.com站点,主要给自己阅读提供方便


## 网站功能

个人不喜欢在微信里面看公账号的文章，太麻烦，历史文章也不方便看，就利用爬虫，加上Flask框架搭建了这个网站，主要内容都是自己订阅的内容，不一定全是公账号的，还有什么值得买和飞客茶馆的一些文章，来源会慢慢增加。
网站还提供了公账号消息的API和RSS订阅。

### 网站链接
1. 主页: <https://vaayne.com>， 暂时显示所有微信公众号的内容，按文章发布时间排序
2. 分类: <https://vaayne.com/category/smzdm>，   <https://vaayne.com/category/flyertea>， 分别显示来自什么值得买和飞客茶馆的文章
3. 微信公众号按作者分类: <https://vaayne.com/wx/(id)> (Id 即为所寻找的微信公众号的id, 区分大小写， 例如小道消息的为<https://vaayne.com/wx/WebNotes>

### RSS
1. 微信公账号: <https://vaayne.com/feed/wx/(id)> 
       id处改为公众号的id(区分大小写)， 比如小道消息的是WebNotes， 则其订阅地址为<https://vaayne.com/feed/wx/WebNotes>
2. 飞客茶馆，飞客知道频道: <https://vaayne.com/feed/flyertea>
3. 什么值得买上的信用卡内容: <http://vaayne.com/feed/smzdm>

### API
#####  微信公众号: 
1. API链接  <https://vaayne.com/api/wx?symbols=(ids)>
        ids 表示的是多个公众号id， 比如想获取小道消息和和菜头的，则其api为<https://vaayne.com/api/wx?symbols=WebNotes,bitsea>
2. 返回
每个账号只返回最近的十篇文章，包括文章正文外的所有文章信息
```javascript
{
	'dates' : {
		'bitsea': [
			{
				'category': '',
				'post_time' : '',
				'title': '',
				'image': '',
				'summary': '',
				'author': '',
				...
			},
			{...},
		]
	},
	'WebNotes': [
		...
	]
}
```

##### 飞客茶馆
<https://vaayne.com/api/flyertea>
返回格式类似微信公众号

##### 什么值得买
<https://vaayne.com/api/smzdm>
返回格式类似微信公众号



## 版本更新

####  Version 1.0 @2016.8.1

主要功能:

    - 微信公众号订阅API
    - 飞客茶馆、什么值得买及微信公众号的抓取
    - 首页显示新闻流

#### Version 1.2 @2016.8.6

What's New：

	- 新增登陆功能
	- 更换微信公众号来源，可以获取到所有的历史文章
	- 增加分类显示，可分别显示来自哪个微信公账号的文章

