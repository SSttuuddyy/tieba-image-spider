from utils import Spieder

if __name__=='__main__':
    print('以Edge浏览器为准')
    y = input('贴子号：')
    sp = Spieder(y)
    num1 = int(input('起始页码：'))
    num2 = int(input('终止页码：'))
    film = input('目标文件夹：')
    page_list=sp.get_page(num2, num1)
    count = num1
    url4 = sp.page_list[0]
    html=sp.get_html(url4)
    name_list = sp.parse_txt(html)
    path = film+'//'+name_list[0]+'//'
    sp.mkdir(path, name_list[0])
    for url in page_list:
        html=sp.get_html(url)
        img_list, title_list=sp.parse_html(html)
        sp.download(path, img_list, title_list)
        print(' 第 %s 页图片下载完成' % count)
        count = count + 1
