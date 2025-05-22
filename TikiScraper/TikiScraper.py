import requests, bs4, re, sqlite3, time
from datetime import datetime

def create_sqlite_database(filename) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print('sqlite3 version:', sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            return conn

def create_tables(conn: sqlite3.Connection):
    sql_statements = [
        """CREATE TABLE IF NOT EXISTS "category"(
            "id" INTEGER NOT NULL UNIQUE,
            "name" TEXT,
            "thumbnail_url" TEXT,
            "link" TEXT,
            "product_count" INTEGER,
            "is_leaf" INTEGER,
            "parent_id" INTEGER,
            PRIMARY KEY("id")
        );""",
        """CREATE TABLE IF NOT EXISTS "product" (
            "id" INTEGER NOT NULL UNIQUE,
            "name" TEXT,
            "link" TEXT,
            "thumbnail_url" TEXT,
            "direct_category" INTEGER,
            "category_path" TEXT,
            "seller_id" INTEGER,
            "seller_name" TEXT,
            "price" REAL,
            "original_price" REAL,
            "discount" REAL,
            "discount_rate" REAL,
            "rating_average" REAL,
            "review_count" INTEGER,
            "inventory_status" TEXT,
            "inventory_type" TEXT,
            "quantity_sold" INTEGER,
            "description" TEXT,
            "brand_name" TEXT,
            "authors" TEXT,
            "specifications" TEXT,
            PRIMARY KEY("id"),
            CONSTRAINT "fk_category" FOREIGN KEY("direct_category") REFERENCES "category"("id") ON UPDATE RESTRICT ON DELETE RESTRICT
        );"""
    ]

    try:
        cursor = conn.cursor()
        for statement in sql_statements:
            cursor.execute(statement)
        
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def add_category(conn, category: tuple):
    try: 
        sql = '''INSERT INTO category(id, name, thumbnail_url, link, product_count, is_leaf, parent_id)
        VALUES(?,?,?,?,?,?,?)'''
        cursor = conn.cursor()
        cursor.execute(sql, category)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(e)
        return -1

def add_product(conn, product: tuple):
    try:
        sql = '''INSERT INTO product(id, name, link, thumbnail_url, direct_category, category_path, seller_id, seller_name, price, original_price, discount, discount_rate, rating_average, review_count, inventory_status, inventory_type, quantity_sold, description, brand_name, authors, specifications)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        cursor = conn.cursor()
        cursor.execute(sql, product)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(e)
        return -1

def add_review(conn, review: tuple):
    try: 
        sql = '''INSERT INTO review(id, product_id, rating, content)
        VALUES(?,?,?,?)'''
        cursor = conn.cursor()
        cursor.execute(sql, review)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(e)
        return -1

def getMenu(conn: sqlite3.Connection, menu_names: list[str]):
    url = "https://api.tiki.vn/raiden/v2/menu-config?platform=desktop"
    payload = {}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    r = requests.request("GET", url, headers=headers, data=payload)
    time.sleep(1)
    data = r.json()
    for c in data['menu_block']['items']:
        if str(c['text']).strip() not in menu_names:
            continue
        last_category = add_category(conn, (str(c['link']).split('/')[-1][1:], c['text'].strip(), c['icon_url'], c['link'], None, False, None))
        print('category', last_category)

def getCategoryIds(conn: sqlite3.Connection) -> list[int]:
    ids = []
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM category')
        rows = cursor.fetchall()
        for row in rows:
            ids.append(row[0])
    except sqlite3.Error as e:
        print(e)
    return ids

def getCategoryChildren(conn: sqlite3.Connection, data: list, parent_id):
    for d in data:
        id = d['id']
        name = str(d['name']).strip('"')
        thumbnail_url = None if 'thumbnail_url' not in d.keys() else d['thumbnail_url']
        link = f'https://tiki.vn/{d["url_key"]}/c{id}'
        product_count = None if 'product_count' not in d.keys() else d['product_count']
        is_leaf = True if 'children' not in d.keys() else False
        last_category = add_category(conn, (id, name, thumbnail_url, link, product_count, is_leaf, parent_id))
        print('category', last_category)

    for d in data:
        if 'children' in d.keys():
            getCategoryChildren(conn, d['children'], d['id'])
    

def getCategories(conn: sqlite3.Connection, menu_ids: list):
    for id in menu_ids:
        url = f"https://tiki.vn/api/v2/categories?include=children&parent_id={id}"

        payload = {}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

        res = requests.request("GET", url, headers=headers, data=payload)
        time.sleep(1)
        data = res.json()['data']
        getCategoryChildren(conn, data, id)

def getCategoryIdsLinksByLeaf(conn: sqlite3.Connection) -> tuple[list[int], list[str]]:
    ids = []
    links = []
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, link FROM category WHERE is_leaf = 1')
        rows = cursor.fetchall()
        for row in rows:
            ids.append(row[0])
            links.append(row[1])
    except sqlite3.Error as e:
        print(e)
    return ids, links

def replace_func(match):
    # Trả về ký tự đầu tiên trong kết quả khớp
    return match.group(0)[0] + " "

def getProductDetails(id: int, link: str) -> dict:
    details = dict()
    spid = str(link).split('=')[-1]
    url = f"https://tiki.vn/api/v2/products/{id}?platform=web&spid={spid}&version=3"

    payload = {}
    headers = {
        'priority': 'u=1, i',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    res = requests.request("GET", url, headers=headers, data=payload)
    time.sleep(1)
    data = res.json()
    details['seller_name'] = data['current_seller']['name'].strip()
    details['price'] = data['price']
    details['original_price'] = data['original_price']
    details['discount'] = data['discount']
    details['discount_rate'] = data['discount_rate']
    details['rating_average'] = data['rating_average']
    details['review_count'] = data['review_count']
    details['inventory_status'] = data['inventory_status'].strip()
    details['inventory_type'] = data['inventory_type'].strip()
    details['quantity_sold'] = 0
    try:
        details['quantity_sold'] = data['all_time_quantity_sold']
    except:
        pass
    description_soup = bs4.BeautifulSoup(data['description'], 'lxml')
    details['description'] = description_soup.get_text(separator='. ', strip=True)
    details['description'] = re.sub(r'[!,.:;?|]\. ', replace_func, details['description'])
    details['brand_name'] = ""
    try:
        details['brand_name'] = data['brand']['name']
    except:
        pass
    details['authors'] = []
    try:
        for author in data['authors']:
            details['authors'].append(author['name'].strip())
    except:
        pass
    details['authors'] = ', '.join(details['authors'])
    details['specifications'] = dict()
    for s in data['specifications']:
        for attr in s['attributes']:
            specifications_soup = bs4.BeautifulSoup(attr['value'], 'lxml')
            specifications = specifications_soup.get_text(separator='. ', strip=True)
            details['specifications'][attr['name']] = re.sub(r'[!,.:;?|]\. ', replace_func, specifications)
    details['specifications'] = str(details['specifications'])
    
    return details

def getProductsByCategory(conn: sqlite3.Connection, category_id: int, category_link: str):
    url = f"https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&aggregations=2&version=home-persionalized&category={category_id}&page=1&urlKey={category_link.split('/')[-2]}"

    payload = {}
    headers = {
        'priority': 'u=1, i',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    res = requests.request("GET", url, headers=headers, data=payload)
    time.sleep(1)
    last_page = res.json()['paging']['last_page']

    for i in range(1, last_page+1):
        url = f"https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&aggregations=2&version=home-persionalized&category={category_id}&page={i}&urlKey={category_link.split('/')[-2]}"
        
        res = requests.request("GET", url, headers=headers, data=payload)
        time.sleep(1)
        data = res.json()['data']
        for d in data:
            id = d['id']
            name = d['name'].strip()
            link = f"https://tiki.vn/{d['url_path']}"

            thumbnail_url = d['thumbnail_url']
            direct_category = category_id
            category_path = str(str(d['primary_category_path']).split('/')[2:])
            seller_id = d['seller_id']
            try:
                details = getProductDetails(id, link)
            except:
                continue
            seller_name = details['seller_name']
            price = details['price']
            original_price = details['original_price']
            discount = details['discount']
            discount_rate = details['discount_rate']
            rating_average = details['rating_average']
            review_count = details['review_count']
            inventory_status = details['inventory_status']
            inventory_type = details['inventory_type']
            quantity_sold = details['quantity_sold']
            description = details['description']
            brand_name = details['brand_name']
            authors = details['authors']
            specifications = details['specifications']

            last_product = add_product(conn, (id, name, link, thumbnail_url, direct_category, category_path, seller_id, seller_name, price, original_price, discount, discount_rate, rating_average, review_count, inventory_status, inventory_type, quantity_sold, description, brand_name, authors, specifications))

            print('product', last_product)

def main(menu_names: list[str]):
    print('Khởi tạo database...', end=' ')
    db_name = 'tiki.db'
    conn = create_sqlite_database(db_name)
    create_tables(conn)
    print('Hoàn thành!')
    
    print('Lấy menu danh mục...')
    getMenu(conn, menu_names)
    print('Hoàn thành!')

    menu_ids = getCategoryIds(conn)
    
    print('Lấy dữ liệu các danh mục...')
    getCategories(conn, menu_ids)
    print('Hoàn thành!')

    del menu_ids

    category_ids, category_links = getCategoryIdsLinksByLeaf(conn)

    print('Lấy dữ liệu các sản phẩm...')
    for i in range(0, len(category_ids)):
        getProductsByCategory(conn, category_ids[i], category_links[i])
    print('Hoàn thành!')

if __name__ == '__main__':
    menu_names = ["Điện Thoại - Máy Tính Bảng", "Laptop - Máy Vi Tính - Linh kiện"]

    menu_names.extend(["Thiết Bị Số - Phụ Kiện Số"])

    menu_names.extend(["Điện Gia Dụng", "Điện Tử - Điện Lạnh", "Máy Ảnh - Máy Quay Phim"])

    start_time = datetime.now()
    main(menu_names)
    end_time = datetime.now()

    print(f'Thời gian bắt đầu: {start_time}')
    print(f'Thời gian kết thúc: {end_time}')
    print(f'Tổng thời gian crawl data Tiki: {end_time - start_time}')
