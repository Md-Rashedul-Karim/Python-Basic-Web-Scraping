import requests
from bs4 import BeautifulSoup
import csv
import random
import time

try:
    # Step 1: Headers - মানুষ এর মত User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    # ওয়েবসাইটের বেস URL
    base_url = "http://books.toscrape.com/"

    # ওয়েবসাইটের URL
    url = base_url

    # ওয়েবপেজ ডাউনলোড করি
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"ওয়েবপেজ ডাউনলোড ব্যর্থ! স্ট্যাটাস কোড: {response.status_code}")
        exit()

    time.sleep(random.uniform(1, 3))
    # নিশ্চিত করি যে রেসপন্স UTF-8 এ পড়া হচ্ছে
    response.encoding = 'utf-8'  # এনকোডিং সেট করি
    print("ওয়েবপেজ ডাউনলোড সফল!")

    # BeautifulSoup দিয়ে HTML পার্স করি
    soup = BeautifulSoup(response.text, "html.parser")


    # সব বইয়ের তথ্য খুঁজে বের করি
    books = soup.find_all("article", class_="product_pod")
    if not books:
        print("কোনো বই পাওয়া যায়নি! HTML স্ট্রাকচার চেক করো।")
        exit()

    # CSV ফাইল তৈরি করি (utf-8-sig এনকোডিং ব্যবহার করি)
    with open("books.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Book Title", "Price", "Book URL", "Image URL", "Rating", "Stock"])  # হেডার in csv

        # Random delay to seem more human-like
        time.sleep(random.uniform(0.2, 0.7))
        # প্রতিটি বইয়ের তথ্য সংগ্রহ করি
        for book in books:
            # বইয়ের নাম
            # title = book.find("h3").find("a")["title"]
            #============= or=====
            title_tag = book.find("h3")
            title = title_tag.find("a")["title"] if title_tag else "N/A"

            # বইয়ের দাম
            # price = book.find("p", class_="price_color").text
            # ============= or=====
            price_tag = book.find("p", class_="price_color")
            price = price_tag.text if price_tag else "N/A"
            # ========== use for multipol class  =============
            stock_tag = book.find("p", class_="instock availability")
            stock = stock_tag.text.strip() if stock_tag else "N/A"
            if stock != "N/A":
                stock = stock.encode('utf-8').decode('utf-8')  # এনকোডিং নিশ্চিত করি
            #========== use for id="stock"=============
            # stock_tag = book.find("p", id="stock")
            # stock = stock_tag.text.strip() if stock_tag else "N/A"
            # if stock != "N/A":
            #     stock = stock.encode('utf-8').decode('utf-8')

            # প্রাইস ক্লিন করি (অপ্রয়োজনীয় ক্যারেক্টার সরাই)
            if price != "N/A":
                price = price.strip()  # অতিরিক্ত স্পেস সরাই
                # যদি এনকোডিং সমস্যা থাকে, তাহলে £ চিহ্ন নিশ্চিত করি
                price = price.encode('utf-8').decode('utf-8')

            # image_container খুঁজি

            image_container = book.find("div", class_="image_container")
            if not image_container:
                print(f"বই '{title}' এর জন্য image_container পাওয়া যায়নি!")
                full_book_url = full_image_url = rating = "N/A"
            else:
                # URL
                # url_tag = image_container.find("a")["href"]
                # print(f"URL: {base_url}{url_tag}")
                # ============= or=====
                url_tag = image_container.find("a")
                book_url = url_tag["href"] if url_tag else "N/A"
                full_book_url = base_url + book_url if book_url != "N/A" else "N/A"

                # Image Path
                img_tag = image_container.find("img")
                image_path = img_tag["src"] if img_tag else "N/A"
                full_image_url = base_url + image_path if image_path != "N/A" else "N/A"

                # Rating
                rating_tag = image_container.find("p", class_="star-rating")
                if rating_tag:
                    try:
                        rating_class = rating_tag["class"][1]  # "One", "Two", ইত্যাদি
                        rating_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                        rating = rating_dict.get(rating_class, "N/A")
                    except (KeyError, IndexError):
                        rating = "N/A"
                else:
                    rating = "N/A"
                    print(f"বই '{title}' এর জন্য রেটিং ট্যাগ পাওয়া যায়নি!")

            # CSV ফাইলে লিখি
            writer.writerow([title, price, full_book_url, full_image_url, rating, stock])
            print(f"সংগ্রহ করা হলো: {title} - {price} - {full_book_url} - {full_image_url} - {rating} - {stock}")

    print("সব তথ্য books.csv ফাইলে সেভ হয়েছে!")
except Exception as err:
    print("Has some error", err)