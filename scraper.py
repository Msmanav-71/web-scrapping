import requests
from bs4 import BeautifulSoup
import csv


# ---------------------------------------
# 1. Website URL
# ---------------------------------------

url = "https://timesofindia.indiatimes.com/news"


# ---------------------------------------
# 2. Browser-like headers
# ---------------------------------------

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/130.0.0.0 Safari/537.36"
}


try:
    # ---------------------------------------
    # 3. Send request to website
    # ---------------------------------------

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )


    # ---------------------------------------
    # 4. Check HTTP status
    # ---------------------------------------

    if response.status_code == 404:
        print("Error 404: Page not found.")

    elif response.status_code >= 500:
        print("Server error:", response.status_code)

    else:
        response.raise_for_status()

        print("Website fetched successfully!")


        # ---------------------------------------
        # 5. Convert HTML into BeautifulSoup
        # ---------------------------------------

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # ---------------------------------------
        # 6. Find all links
        # ---------------------------------------

        links = soup.find_all("a")


        news_data = []


        # ---------------------------------------
        # 7. Extract title and link
        # ---------------------------------------

        for link in links:

            title = link.get_text(" ", strip=True)

            href = link.get("href")


            # Ignore empty links
            if not title or not href:
                continue


            # Convert relative URL to full URL
            if href.startswith("/"):
                href = "https://timesofindia.indiatimes.com" + href


            # Store data
            news_data.append({
                "title": title,
                "link": href
            })


        # ---------------------------------------
        # 8. Remove duplicate links
        # ---------------------------------------

        unique_data = []

        seen_links = set()


        for item in news_data:

            if item["link"] not in seen_links:

                seen_links.add(item["link"])

                unique_data.append(item)


        # ---------------------------------------
        # 9. Save data into CSV
        # ---------------------------------------

        with open(
            "toi_news.csv",
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=["title", "link"]
            )

            writer.writeheader()

            writer.writerows(unique_data)


        print("Scraping completed!")

        print("Saved file: toi_news.csv")

        print("Total records:", len(unique_data))


except requests.exceptions.Timeout:

    print("Error: Website request timed out.")


except requests.exceptions.ConnectionError:

    print("Error: Internet connection problem.")


except requests.exceptions.HTTPError as error:

    print("HTTP Error:", error)


except requests.exceptions.RequestException as error:

    print("Request failed:", error)