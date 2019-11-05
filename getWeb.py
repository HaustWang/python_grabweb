#coding:utf-8
import urllib
import re
import os

def get_html(url):
    page = urllib.urlopen(url)
    htmlcode = page.read()
    return htmlcode

def write_file(url, filename, path=""):
    if(os.path.exists(filename)):
        return
    if(path != ""):
        if(not os.path.exists(path)):
            os.makedirs(path)
        if(filename.find(path) == -1):
            filename = path + filename
    if(url.find('http:') == -1):
        url = "http:" + url
    urllib.urlretrieve(url, filename)

def proc_file(reg, html, path, outrel):
    reg_file = re.compile(reg)
    filelist = reg_file.findall(html)
    if(not os.path.exists(path)):
        os.makedirs(path)
    for ff in filelist:
        print ff
        filename = path + ff[ff.rindex("/")+1:]
        print filename
        write_file(ff, filename)
        if filename.find(outrel) == 0:
            html = replace_html(html, ff, filename)
        else:
            html = replace_html(html, ff, outrel + filename)
    return html

def get_pic(html, outrel):
    reg = r'src="(//image\S+\.jpg)" '
    html = proc_file(reg, html, './image/', outrel)
    
    reg = r'src="(//image\S+\.png)" '
    html = proc_file(reg, html, './image/', outrel)

    reg = r'href="(//image\S+\.ico)" '
    html = proc_file(reg, html, './image/', outrel)

    return html

def get_css(html, outrel):
    reg = r'href="(\S+\.css)" '
    return proc_file(reg, html, './css/', outrel)

def get_js(html, outrel):
    reg = r'src="(\S+\.js)"'
    return proc_file(reg, html, './js/', outrel)

def proc_font(font):
    reg = r'/(\d+/\S+)'
    reg_font = re.compile(reg)
    fontpaths = reg_font.findall(font)
    for fontpath in fontpaths:
        endidx = fontpath.rfind('?')
        if endidx == -1:
            endidx = len(fontpath) 

        filename = './font/' + fontpath[:endidx]
        print filename
        filenameidx = filename.rfind('/')
        path = ""
        if(filenameidx != -1):
            path = filename[0:filenameidx+1]
            filename = filename[filenameidx+1:]
        #print filename, path  
        write_file(font, filename, path)

def get_font():
    for dirpath,dirnames,filenames in os.walk('./css'):
        for f in filenames:
            filepath = dirpath + "/" + f
            ff = open(filepath)
            ff1 = open(filepath + "_tmp", "w")
            while 1:
                line = ff.readline()
                if not line:
                    break
                reg = r'url\((//\S+)\);'
                reg_font = re.compile(reg)
                fontlist = reg_font.findall(line)
                for font in fontlist:
                    proc_font(font) 

                reg = r',url\((//\S+)\)'
                reg_font = re.compile(reg)
                fontlist = reg_font.findall(line)
                for font in fontlist:
                    proc_font(font)

                line = replace_html(line, "//static.eostatic.com/theme/themes/commons/font/", "../font/");
                line = replace_html(line, "//static.eostatic.com/theme/themes/", "../font/");

                ff1.write(line)
            ff.close()
            ff1.close()
            os.remove(filepath)
            os.rename(filepath + "_tmp", filepath)


def write_web(html_code, outfile):
        pageFile = open(outfile, "w")
        pageFile.write(html_code)
        pageFile.close()

    
def replace_html(html_code, old_str, new_str):
        html_code = html_code.replace(old_str, new_str)
        #print "replace_html", html_code
        return html_code

def replace_html_re(html_code, reg, new_str):
    reg_old = re.compile(reg)
    html_code = reg_old.sub(new_str, html_code)
    return html_code
        

def getWeb(url, langs=[], htmls=[]):
        outrel = './'
        if not langs:
            langs = ["en"];
        if not htmls:
            htmls = [];
        for lang in langs:
            if lang == "en":
                outrel = "./"
            else:
                outrel = "../"

            for html in htmls:
                outfile = "./" + lang + "/" + html
                if lang == "en":
                    outfile = "./" + html
                    
                html_url = "http:" + url + "/" + lang + "/" + html
                if html == "index.html":
                    html_url = "http:" + url + "/" + lang
 
                html_code = get_html(html_url)
                html_code = get_pic(html_code, outrel)
                html_code = get_css(html_code, outrel)
                html_code = get_js(html_code, outrel)
                        
                html_code = replace_html(html_code, "<div class=\"menu-item menu-currency dropdown\" data-dropdown=\"hover\"><div class=\"menu-title\" data-toggle=\"dropdown\"><span class=\"ico-flag ico-flag-usd\"></span>USD<span class=\"ico-arrow-down\"></span></div><div class=\"menu-pane dropdown-menu\"><ul class=\"menu-list\"><li><a href=\"javascript:void(0);\" data-currency=\"AUD\"><span class=\"ico-flag ico-flag-aud\"></span>AUD</a></li><li><a href=\"javascript:void(0);\" data-currency=\"BRL\"><span class=\"ico-flag ico-flag-brl\"></span>BRL</a></li><li><a href=\"javascript:void(0);\" data-currency=\"CAD\"><span class=\"ico-flag ico-flag-cad\"></span>CAD</a></li><li><a href=\"javascript:void(0);\" data-currency=\"CHF\"><span class=\"ico-flag ico-flag-chf\"></span>CHF</a></li><li><a href=\"javascript:void(0);\" data-currency=\"CNY\"><span class=\"ico-flag ico-flag-cny\"></span>CNY</a></li><li><a href=\"javascript:void(0);\" data-currency=\"EUR\"><span class=\"ico-flag ico-flag-eur\"></span>EUR</a></li><li><a href=\"javascript:void(0);\" data-currency=\"GBP\"><span class=\"ico-flag ico-flag-gbp\"></span>GBP</a></li><li><a href=\"javascript:void(0);\" data-currency=\"HKD\"><span class=\"ico-flag ico-flag-hkd\"></span>HKD</a></li><li><a href=\"javascript:void(0);\" data-currency=\"INR\"><span class=\"ico-flag ico-flag-inr\"></span>INR</a></li><li><a href=\"javascript:void(0);\" data-currency=\"JPY\"><span class=\"ico-flag ico-flag-jpy\"></span>JPY</a></li><li><a href=\"javascript:void(0);\" data-currency=\"KRW\"><span class=\"ico-flag ico-flag-krw\"></span>KRW</a></li><li><a href=\"javascript:void(0);\" data-currency=\"MXN\"><span class=\"ico-flag ico-flag-mxn\"></span>MXN</a></li><li><a href=\"javascript:void(0);\" data-currency=\"RUB\"><span class=\"ico-flag ico-flag-rub\"></span>RUB</a></li><li><a href=\"javascript:void(0);\" data-currency=\"USD\"><span class=\"ico-flag ico-flag-usd\"></span>USD</a></li><li><a href=\"javascript:void(0);\" data-currency=\"TWD\"><span class=\"ico-flag ico-flag-twd\"></span>TWD</a></li><li><a href=\"javascript:void(0);\" data-currency=\"THB\"><span class=\"ico-flag ico-flag-thb\"></span>THB</a></li></ul></div></div>", "");
                html_code = replace_html(html_code, '<div class="menu-item menu-currency dropdown" data-dropdown="hover"><div class="menu-title" data-toggle="dropdown"><span class="ico-flag ico-flag-cny"></span>CNY<span class="ico-arrow-down"></span></div><div class="menu-pane dropdown-menu"><ul class="menu-list"><li><a href="javascript:void(0);" data-currency="AUD"><span class="ico-flag ico-flag-aud"></span>AUD</a></li><li><a href="javascript:void(0);" data-currency="BRL"><span class="ico-flag ico-flag-brl"></span>BRL</a></li><li><a href="javascript:void(0);" data-currency="CAD"><span class="ico-flag ico-flag-cad"></span>CAD</a></li><li><a href="javascript:void(0);" data-currency="CHF"><span class="ico-flag ico-flag-chf"></span>CHF</a></li><li><a href="javascript:void(0);" data-currency="CNY"><span class="ico-flag ico-flag-cny"></span>CNY</a></li><li><a href="javascript:void(0);" data-currency="EUR"><span class="ico-flag ico-flag-eur"></span>EUR</a></li><li><a href="javascript:void(0);" data-currency="GBP"><span class="ico-flag ico-flag-gbp"></span>GBP</a></li><li><a href="javascript:void(0);" data-currency="HKD"><span class="ico-flag ico-flag-hkd"></span>HKD</a></li><li><a href="javascript:void(0);" data-currency="INR"><span class="ico-flag ico-flag-inr"></span>INR</a></li><li><a href="javascript:void(0);" data-currency="JPY"><span class="ico-flag ico-flag-jpy"></span>JPY</a></li><li><a href="javascript:void(0);" data-currency="KRW"><span class="ico-flag ico-flag-krw"></span>KRW</a></li><li><a href="javascript:void(0);" data-currency="MXN"><span class="ico-flag ico-flag-mxn"></span>MXN</a></li><li><a href="javascript:void(0);" data-currency="RUB"><span class="ico-flag ico-flag-rub"></span>RUB</a></li><li><a href="javascript:void(0);" data-currency="USD"><span class="ico-flag ico-flag-usd"></span>USD</a></li><li><a href="javascript:void(0);" data-currency="TWD"><span class="ico-flag ico-flag-twd"></span>TWD</a></li><li><a href="javascript:void(0);" data-currency="THB"><span class="ico-flag ico-flag-thb"></span>THB</a></li></ul></div></div>', "")
                html_code = replace_html(html_code, "<div style=\"padding: 9px 0;\"><div style=\"position: relative;display: inline-block;width:250px;height: 25px;margin-right: 4px;vertical-align: middle;\"><img style=\"width:100%;\" src=\"//static.eostatic.com/common/trial/text.png\" /><img style=\"position: absolute;top: 1px;left: 82px;width: 130px;\" src=\"//static.eostatic.com/common/logo/logo_eo_l.png\" /></div><a style=\"display:inline-block;width:80px;height:22px;overflow: hidden;vertical-align: middle;\" href=\"//admin.easyofficial.com/\"><img style=\"display:block;width:80px;\" src=\"//static.eostatic.com/common/trial/btn.png\" onmouseenter=\"this.style.marginTop='-22px'\" onmouseleave=\"this.style.marginTop='0'\" /></a></div></div><script>;(function(){var w=window;w.easyofficial_track=w.easyofficial_track||function(){(w.easyofficial_track.q=w.easyofficial_track.q||[]).push(arguments);};easyofficial_track('create',{baidu_push:true,google_tracking_id:'',google_conversion_id:'',bing_tag_id:'',facebook_pixel_id:'',easyofficial_collect:'http://a.eostatic.com/collect',easyofficial_uid:'3B44C15C-B8CC-6597-4DB6-0D9E7C56B5B8',easyofficial_sid:'BEBD936B-9724-D10B-2F88-AD1C208BD48F',easyofficial_timestamp:1543825621});easyofficial_track('easyofficial_analytics', {category:'pv',merchant_id:'5148'});w.easyofficial_track.t=1*new Date();}());</script>", "")
                html_code = replace_html(html_code, '<div style="padding: 9px 0;"><div style="position: relative;display: inline-block;width:250px;height: 25px;margin-right: 4px;vertical-align: middle;"><img style="width:100%;" src="//static.eostatic.com/common/trial/text.png" /><img style="position: absolute;top: 1px;left: 82px;width: 130px;" src="//static.eostatic.com/common/logo/logo_eo_l.png" /></div><a style="display:inline-block;width:80px;height:22px;overflow: hidden;vertical-align: middle;" href="//admin.easyofficial.com/"><img style="display:block;width:80px;" src="//static.eostatic.com/common/trial/btn.png" onmouseenter="this.style.marginTop=\'-22px\'" onmouseleave="this.style.marginTop=\'0\'" /></a></div>', "")

                reg = r'\<script\>;\(function\(\)\{var.+Date\(\);\}\(\)\);\</script\>'
                html_code = replace_html_re(html_code, reg, "")

                reg = r'\<li class=\"foldmenu\"\>\<a href=\"javascript:void\(0\);\" data-toggle=\"foldmenu\"\>.+EULA\</a\>\</li\>\</ul\>\</li\>'
                html_code = replace_html_re(html_code, reg, "")

                reg = r'\<li class=\"dropdown\" data-dropdown=\"hover\"\>\<a href=\"javascript:void\(0\);\" data-toggle=\"dropdown\"\>.+EULA\</a\>\</li\>\</ul\>\</li\>'
                html_code = replace_html_re(html_code, reg, "")

                reg = r'\<div class=\"item item-newsletter\"\>.+\</span\>\</div\>\</div\>\</div\>\</div\>\</div\>'
                html_code = replace_html_re(html_code, reg, '</div></div></div>')

                reg = r'\<li class=\"weixin\"\>[\s\S]*\<li class=\"google\"\>'
                html_code = replace_html_re(html_code, reg, '<li class="google">');

                reg = r'\<div class=\"menu-item menu-lang dropdown\".+\</ul\>\</div\>\</div\>\</div\>\</div\>\</div\>\<div class=\"nav-bottom-logo\"\>'
                if lang == "en":
                    html_code = replace_html_re(html_code, reg, '<div class="menu-item menu-lang dropdown" data-dropdown="hover"><div class="menu-title" data-toggle="dropdown">English<span class="ico-arrow-down"></span> </div><div class="menu-pane dropdown-menu"><ul class="menu-list"><li><a href="./zh/' + html + '">中文</a></li><li><a href="./tw/' + html + '">繁體中文</a></li></ul></div></div></div></div></div><div class="nav-bottom-logo">')
                    html_code = replace_html(html_code, '<div class="copyright">', '<div id="footer-links"><ul><li><a target="_self" href="./terms-of-service-s3.html">Term of Service</a></li><li><a target="_self" href="./private-policy-s4.html">Privacy Policy</a></li><li><a target="_self" href="./gdpr-s5.html">GDPR</a></li><li><a target="_self" href="./eula-s6.html">EULA</a></li></ul></div><div class="copyright">')
                    html_code = replace_html(html_code, '<div class="item"><div class="title ellipsis">Quick Links</div><ul class="info"><li class="ellipsis"><a target="_blank" href="javascript:void(0);">FAQ</a></li><li class="ellipsis"><a target="_blank" href="javascript:void(0);">SEARCH</a></li></ul></div>', '')
                elif lang == "zh":
                    html_code = replace_html_re(html_code, reg, '<div class="menu-item menu-lang dropdown" data-dropdown="hover"><div class="menu-title" data-toggle="dropdown">中文<span class="ico-arrow-down"></span> </div><div class="menu-pane dropdown-menu"><ul class="menu-list"><li><a href="../' + html + '">English</a></li><li><a href="../tw/' + html + '">繁體中文</a></li></ul></div></div></div></div></div><div class="nav-bottom-logo">')
                    html_code = replace_html(html_code, '<div class="copyright">', '<div id="footer-links"><ul><li><a target="_self" href="./terms-of-service-s3.html">服务期限</a></li><li><a target="_self" href="./private-policy-s4.html">隐私政策</a></li><li><a target="_self" href="./gdpr-s5.html">GDPR</a></li><li><a target="_self" href="./eula-s6.html">EULA</a></li></ul></div><div class="copyright">')
                    html_code = replace_html(html_code, '<div class="item"><div class="title ellipsis">快速链接</div><ul class="info"><li class="ellipsis"><a target="_blank" href="javascript:void(0);">常见问题</a></li><li class="ellipsis"><a target="_blank" href="javascript:void(0);">搜索</a></li></ul></div>', '')
                elif lang == "tw":
                    html_code = replace_html_re(html_code, reg, '<div class="menu-item menu-lang dropdown" data-dropdown="hover"><div class="menu-title" data-toggle="dropdown">繁體中文<span class="ico-arrow-down"></span> </div><div class="menu-pane dropdown-menu"><ul class="menu-list"><li><a href="../' + html + '">English</a></li><li><a href="../zh/' + html + '">中文</a></li></ul></div></div></div></div></div><div class="nav-bottom-logo">')
                    html_code = replace_html(html_code, '<div class="copyright">', '<div id="footer-links"><ul><li><a target="_self" href="./terms-of-service-s3.html">服務期限</a></li><li><a target="_self" href="./private-policy-s4.html">隱私政策</a></li><li><a target="_self" href="./gdpr-s5.html">GDPR</a></li><li><a target="_self" href="./eula-s6.html">EULA</a></li></ul></div><div class="copyright">')
                    html_code = replace_html(html_code, '<div class="item"><div class="title ellipsis">快速鏈接</div><ul class="info"><li class="ellipsis"><a target="_blank" href="javascript:void(0);">常見問題</a></li><li class="ellipsis"><a target="_blank" href="javascript:void(0);">搜索</a></li></ul></div>', '')
                    
                if lang == "en":
                    html_code = replace_html(html_code, url + "/", "./");
                    html_code = replace_html(html_code, url, "./index.html");
                else:
                    html_code = replace_html(html_code, url + "/" + lang + "/", "./");
                    html_code = replace_html(html_code, url + "/" + lang, "./index.html");

                html_code = replace_html(html_code, '</body>', '</body>' + '<style>#footer-links{position: relative;bottom: 0px;z-index: 10000;width: 100%;} #footer-links ul li{list-style:none;margin-right:5px;margin-left:5px;display:inline;} #footer-links ul li:after{content: "";height: 100%;width: 10px;border: 1px solid #000;margin-left: 10px;} #footer-links ul li:last-child:after {content: "";height: 100%;width: 10px;border: 0px solid #000;margin-left: 10px;} #footer-links a{color: #000;}</style>')
                html_code = replace_html(html_code, './' + lang + '"', './' + lang + '/index.html"')
                write_web(html_code, outfile)

def main():
    getWeb("//ivf2d9ifndk.globalsite.cc", ["en", "zh"], ["index.html", "games-s2.html","contact-us-s1.html", "terms-of-service-s3.html", "private-policy-s4.html", "gdpr-s5.html", "eula-s6.html"])
    get_font()

if __name__ == '__main__':
        main()

