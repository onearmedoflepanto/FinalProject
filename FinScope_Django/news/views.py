from django.http import JsonResponse
from django.views.decorators.http import require_GET
import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


@require_GET
def scrape_news_view(request):
    news_url = request.GET.get("url")

    if not news_url:
        return JsonResponse({"error": "URL parameter is missing"}, status=400)

    scraped_title = f"News Article from {urlparse(news_url).hostname}"  # Default title
    scraped_content = f"Placeholder content for {news_url}. Implement full scraping."
    scraped_image_url = f"https://placehold.co/600x400.png?text=News+from+{urlparse(news_url).hostname.replace('.', '+')}"
    source_host = (
        urlparse(news_url).hostname if urlparse(news_url).hostname else "Unknown source"
    )

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(news_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, "html.parser")

        # Try to find the title tag
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            scraped_title = title_tag.string.strip()

        # NOTE: Scraping main content and image is more complex and site-specific.
        # The following are still placeholders. You would need to identify
        # specific tags or classes for the main article body and image on target sites.
        # For example, you might look for <meta property="og:image" content="..."> for an image.
        # Or <article> tags, or divs with class="article-content" for content.

        # Example for OpenGraph image (common but not guaranteed)
        og_image_tag = soup.find("meta", property="og:image")
        og_image_content = og_image_tag.get("content") if og_image_tag else None
        if og_image_content:
            scraped_image_url = og_image_content

        # Attempt to find main article content by trying common selectors
        content_selectors = [
            "article",  # General semantic tag
            ".article-body",  # Common class name
            ".story-content",  # Another common one
            ".main-content",  # Often used for the primary content area
            ".entry-content",  # WordPress and other CMSs
            'div[itemprop="articleBody"]',  # Schema.org microdata
            ".article_body",  # Variation
            ".article__content",  # BEM style
            ".news_article_body",  # Specific to news
            "#article_body",  # Common ID
            "#content",  # Generic ID, might be too broad but worth a try
            "#main",  # Generic ID
            ".td-post-content",  # Newspaper/magazine themes
            ".post-content",  # Blog themes
        ]

        # Site-specific selectors can be added here
        if source_host == "www.newstomato.com":
            # Based on user XPath: /html/body/div[1]/div/main/div/div/p
            # Parent container selector:
            newstomato_selector = "body > div:nth-of-type(1) > div > main > div > div"
            # Prepend so it's tried first for this specific domain
            content_selectors.insert(0, newstomato_selector)
            # print(f"Using specific selector for newstomato.com: {newstomato_selector}") # 디버깅용 print 제거

        article_content_element = None
        for selector in content_selectors:
            try:
                article_content_element = soup.select_one(selector)
                if article_content_element:
                    break
            except (
                Exception
            ) as e_select:  # Catch potential errors from complex selectors
                # print(f"Selector error for '{selector}': {e_select}") # 디버깅용 print 제거
                continue

        if article_content_element:
            # Remove known irrelevant sections (very basic example)
            # These selectors should be relative to article_content_element if possible, or global if necessary
            irrelevant_selectors_in_content = [
                ".related-articles",
                ".comments-section",
                ".author-bio",
                ".share-buttons",
                ".ad-container",
            ]
            for irrelevant_selector in irrelevant_selectors_in_content:
                for tag in article_content_element.select(irrelevant_selector):
                    tag.decompose()  # Remove the tag and its content

            # Also try to remove common global irrelevant tags if they are mistakenly included
            # This is less precise and should be used cautiously
            # for tag_name in ['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']:
            #    for tag in article_content_element.find_all(tag_name):
            #        tag.decompose()

            paragraphs = article_content_element.find_all(
                "p", recursive=True
            )  # Get all p tags, even nested
            if paragraphs:
                # Join text from paragraphs, ensuring they are not empty and stripping extra whitespace
                scraped_content = "\n\n".join(
                    p.get_text(separator=" ", strip=True)
                    for p in paragraphs
                    if p.get_text(strip=True)
                )
            else:
                # Fallback to getting all text if no <p> tags found within the selected element
                scraped_content = article_content_element.get_text(
                    separator="\n", strip=True
                )
        else:
            # Fallback if no specific container found: try all p tags in body (less reliable)
            # This was the previous less effective method, kept as a last resort
            body_paragraphs = soup.body.find_all("p") if soup.body else []
            if body_paragraphs:
                scraped_content = "\n\n".join(
                    p.get_text(separator=" ", strip=True)
                    for p in body_paragraphs
                    if p.get_text(strip=True)
                )

        # Final check if content is still placeholder or empty or too short
        if (
            not scraped_content.strip()
            or scraped_content.startswith("Placeholder content for")
            or len(scraped_content.strip()) < 150
        ):  # Increased minimum length for meaningful content
            scraped_content = f"Could not automatically extract sufficient main content for {news_url}. The site structure might be too complex for generic scraping, or the content is primarily non-textual. Specific parsing rules may be needed for this website."

    except requests.exceptions.RequestException as e:
        # print(f"Error fetching URL {news_url}: {e}") # 디버깅용 print 제거
        # Keep default title and content if scraping fails
        scraped_content = (
            f"Could not fetch or parse the news article from {news_url}. Error: {e}"
        )
    except Exception as e:
        # print(f"An unexpected error occurred during scraping {news_url}: {e}") # 디버깅용 print 제거
        scraped_content = f"An unexpected error occurred while trying to process the news from {news_url}."

    data = {
        "title": scraped_title,
        "source": source_host,
        "publishedAt": datetime.datetime.now().isoformat(),  # Placeholder, real date needs scraping
        "content": scraped_content,  # Still largely placeholder, needs robust scraping
        "imageUrl": scraped_image_url,  # Might be a real image if OG tag found, else placeholder
        "originalLink": news_url,
    }

    return JsonResponse(data)
