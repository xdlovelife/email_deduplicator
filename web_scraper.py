import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse

def scrape_website(url):
    try:
        # 发送GET请求
        response = requests.get(url)
        response.raise_for_status()  # 如果请求不成功则抛出异常
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取信息
        title = soup.title.string if soup.title else "无标题"
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else "无描述"
        
        # 提取所有链接
        links = [a['href'] for a in soup.find_all('a', href=True)]
        
        # 提取所有图片URL
        images = [img['src'] for img in soup.find_all('img', src=True)]
        
        # 获取网站的域名
        domain = urlparse(url).netloc
        
        return {
            "url": url,
            "title": title,
            "description": description,
            "domain": domain,
            "links": links,
            "images": images
        }
    except requests.RequestException as e:
        print(f"抓取 {url} 时发生错误: {e}")
        return None

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "标题", "描述", "域名", "链接数", "图片数"])
        writer.writerow([
            data["url"],
            data["title"],
            data["description"],
            data["domain"],
            len(data["links"]),
            len(data["images"])
        ])

if __name__ == "__main__":
    url = input("请输入要抓取的网站URL: ")
    data = scrape_website(url)
    if data:
        print(f"标题: {data['title']}")
        print(f"描述: {data['description']}")
        print(f"域名: {data['domain']}")
        print(f"链接数: {len(data['links'])}")
        print(f"图片数: {len(data['images'])}")
        
        save_to_csv(data, "website_info.csv")
        print("数据已保存到 website_info.csv")
    else:
        print("抓取失败")
