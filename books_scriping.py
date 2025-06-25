# ওয়েব স্ক্র্যাপিং প্রজেক্ট - বই এর তথ্য সংগ্রহ
"""
এই প্রজেক্টে আমরা http://books.toscrape.com থেকে বই এর তথ্য সংগ্রহ করবো
এটি একটি টেস্ট ওয়েবসাইট যেটি স্ক্র্যাপিং অনুশীলনের জন্য বানানো হয়েছে
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import pdb


def scrape_books():
    """
    বই এর তথ্য স্ক্র্যাপ করার ফাংশন
    """
    print("🚀 স্ক্র্যাপিং শুরু হচ্ছে...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    # ওয়েবসাইটের URL
    url = "http://books.toscrape.com/"

    try:
        # ওয়েবসাইটে রিকুয়েস্ট পাঠানো
        print("📡 ওয়েবসাইটে সংযোগ করা হচ্ছে...")
        response = requests.get(url, headers=headers)

        # সংযোগ সফল হয়েছে কিনা চেক করা
        if response.status_code == 200:
            print("✅ সংযোগ সফল!")
        else:
            print(f"❌ সংযোগ ব্যর্থ! Status Code: {response.status_code}")
            return

        # HTML কোড পার্স করা
        soup = BeautifulSoup(response.content, 'html.parser')

        # বই এর তথ্য সংগ্রহ করার জন্য লিস্ট
        books_data = []

        # সব বই খুঁজে বের করা
        books = soup.find_all('article', class_='product_pod')

        # print(f"📚 মোট {len(books)} টি বই পাওয়া গেছে!")

        # প্রতিটি বই থেকে তথ্য সংগ্রহ করা
        for i, book in enumerate(books, 1):
            try:
                # বই এর নাম
                title = book.find('h3').find('a')['title']

                # বই এর দাম
                # price = book.find('p', class_='price_color').text
                price_tag = book.find("p", class_="price_color")
                price = price_tag.text if price_tag else "N/A"
                if price != "N/A":
                    price = price.strip(" ")  # অতিরিক্ত স্পেস সরাই or remove "£"
                    # যদি এনকোডিং সমস্যা থাকে, তাহলে £ চিহ্ন নিশ্চিত করি
                    price = price.encode('utf-8').decode('utf-8')

                image_container = book.find("div", class_="image_container")
                if not image_container:
                    print(f"বই '{title}' এর জন্য image_container পাওয়া যায়নি!")
                else:
                    # URL
                    # url_tag = image_container.find("a")["href"]
                    # print(f"URL: {base_url}{url_tag}")
                    # ============= or=====
                    url_tag = image_container.find("a")
                    book_url = url_tag["href"] if url_tag else "N/A"
                    full_book_url = url + book_url if book_url != "N/A" else "N/A"

                    # Image Path
                    img_tag = image_container.find("img")
                    image_path = img_tag["src"] if img_tag else "N/A"
                    full_image_url = url + image_path if image_path != "N/A" else "N/A"


                # বই এর rating
                rating_classes = book.find('p', class_='star-rating')['class']
                rating = rating_classes[1]  # 'One', 'Two', 'Three', 'Four', 'Five'

                # বই এর স্টক স্ট্যাটাস
                stock = book.find('p', class_='instock availability').text.strip()

                # ডিকশনারিতে তথ্য সংরক্ষণ
                book_info = {
                    'name': title,
                    'price': price,
                    'book_url': full_book_url,
                    'image': full_image_url,
                    'rating': rating,
                    'stock': stock
                }

                books_data.append(book_info)
                print(f"📖 বই {i}: {title[:30]}...")

                # সার্ভারে অতিরিক্ত চাপ না দেওয়ার জন্য বিরতি
                time.sleep(0.1)

            except Exception as e:
                print(f"❌ বই {i} প্রসেস করতে সমস্যা: {e}")
                continue

        return books_data

    except Exception as e:
        print(f"❌ স্ক্র্যাপিং এ সমস্যা: {e}")
        return []


def save_to_csv(books_data, filename='books_data.csv'):
    """
    বই এর তথ্য CSV ফাইলে সংরক্ষণ করা
    """
    if books_data:
        df = pd.DataFrame(books_data)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"💾 তথ্য '{filename}' ফাইলে সংরক্ষিত হয়েছে!")
        return True
    else:
        print("❌ সংরক্ষণ করার মতো কোনো তথ্য নেই!")
        return False



def main():
    """
    মূল ফাংশন
    """
    print("🎯 ওয়েব স্ক্র্যাপিং প্রজেক্ট")
    print("=" * 50)

    # বই এর তথ্য স্ক্র্যাপ করা
    books_data = scrape_books()

    if books_data:
        print(f"\n🎉 সফলভাবে {len(books_data)} টি বই এর তথ্য সংগ্রহ করা হয়েছে!")


        # CSV ফাইলে সংরক্ষণ করা
        save_to_csv(books_data)

        # কিছু পরিসংখ্যান দেখানো
        print("\n📊 পরিসংখ্যান:")
        print(f"   মোট বই: {len(books_data)}")

        # priceের ভিত্তিতে বিশ্লেষণ
        prices = [float(book['price'][1:]) for book in books_data]  # £ চিহ্ন বাদ দিয়ে
        print(f"   সর্বোচ্চ price: £{max(prices):.2f}")
        print(f"   সর্বনিম্ন price: £{min(prices):.2f}")
        print(f"   গড় price: £{sum(prices) / len(prices):.2f}")

    else:
        print("❌ কোনো তথ্য সংগ্রহ করা যায়নি!")


# প্রয়োজনীয় লাইব্রেরি ইনস্টল করার জন্য কমান্ড:
"""
pip install requests beautifulsoup4 pandas
"""

if __name__ == "__main__":
    main()