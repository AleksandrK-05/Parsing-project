import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def parse_pedsovet_articles():
    """
    Парсинг карточек статей с сайта pedsovet.org
    """
    url = "https://pedsovet.org/"
    
    try:
        
        print(" Загружаем страницу...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Создаем объект с таким же названием, чтобы было удобнен
        soup = BeautifulSoup(response.text, 'html.parser')
        articles_data = []
        

        print(" Ищем карточки статей...")
        cards = soup.find_all('div', class_=lambda x: x and any(word in str(x) for word in ['card', 'item', 'news', 'article', 'post']))
        
        # другой поиск, если там не получилось
        if not cards:
            cards = soup.select('div[class*="card"], div[class*="item"], div[class*="news"]')
        
        print(f" Найдено карточек: {len(cards)}")
        
        for i, card in enumerate(cards, 1):
            try:
                # тут ищутся заголовки
                title_elem = card.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'span', 'div'])
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 5:
                    continue
                
                # тут ищется ссылка
                link_elem = card.find('a', href=True)
                if link_elem:
                    link = link_elem['href']
                    if link.startswith('/'):
                        link = urljoin(url, link)
                else:
                    link = "Ссылка не найдена"
                
                # тут просто добавляем данные 
                articles_data.append({
                    'id': i,
                    'title': title,
                    'link': link
                })
                
                print(f" Обработана карточка {i}: {title[:50]}...")
                
            except Exception as e:
                print(f" Ошибка в карточке {i}: {e}")
                continue
        
        # тут вывода результата
        print("\n" + "="*60)
        print(" РЕЗУЛЬТАТЫ ПАРСИНГА:")
        print("="*60)
        
        for article in articles_data:
            print(f" {article['title']}")
            print(f"🔗 {article['link']}")
            print()
        
        # тут сохраняем файл в json 
        with open('pedsovet_articles.json', 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=2)
        
        print(f" Данные сохранены в: pedsovet_articles.json")
        print(f" Всего статей: {len(articles_data)}")
        
        return articles_data
        
    except requests.RequestException as e:
        print(f" Ошибка загрузки: {e}")
        return []
    except Exception as e:
        print(f" Общая ошибка: {e}")
        return []

if __name__ == "__main__":

    parse_pedsovet_articles()

