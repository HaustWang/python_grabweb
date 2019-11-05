# python_grabweb

这个里面包含两个文件：

get_doc.py 出自同事SSX之手，主要用于从网上扒拉书籍，使用方式如下：
一、应用场景
爬取网站上的分页资料，合并后转为pdf，支持简单的session验证


二、前期准备
1.python及相关的库
	pip install PyPDF2
	pip install requests
	pip install beautifulsoup4
	pip install pdfkit
2.安装wkhtmltopdf
	sudo yum intsall wkhtmltopdf
3.为了保证wkhtmltopdf可用
	a. 安装宋体字体库
		yum -y install fontconfig
		网上随便找到一个simsun.ttc扔到/usr/share/fonts下
	b. 安裝xvfb
	    yum install xorg-x11-server-Xvfb
	c. Using wkhtmltopdf with X server
		printf '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*' > /usr/bin/wkhtmltopdf.sh
		chmod a+x /usr/bin/wkhtmltopdf.sh
		ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf

三、使用
	headers当中的内容,在chrome浏览器中F12 -> Network中寻找
	其它网页源代码在F12 -> Elements中寻找
	get_url_list函数为获取所有待采集的url方法，一般可以在类似 “下一章” “下一页”相关标签处找到该url，然后使用BS4的css选择器，得到这个url
	parse_url_to_html函数为访问url并解析html,这里使用css选择器,获取正文标签和标题标签
  
getWeb.py，主要是从三方制作的公司官网，自己扒拉下来该写之后放在公司官网上。这两个工具都只是作为自己学习使用，上传记录下来。
