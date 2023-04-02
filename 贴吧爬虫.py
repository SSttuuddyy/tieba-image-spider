from utils import Spieder

if __name__=='__main__':
    y = input('贴子号：')
    sp = Spieder(y)
    num1 = int(input('起始页码：'))
    num2 = int(input('终止页码：'))
    film = input('目标文件夹：')
    page_list=sp.get_page(num2, num1)
    count = num1
    for url in page_list:
        html=sp.get_html(url)
        img_list, title_list=sp.parse_html(html)
        sp.download(film, img_list, title_list)
        print(' 第 %s 页图片下载完成' % count)
        print('下载完成第{0}张图片'.format(count))
        count = count + 1
