from django.test import TestCase
from news_app.models import Article
from django.utils import timezone

# title description, url, pub_date, image
class ArticleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        new_article = Article.objects.create(
            id=1,
            title="New article",
            description="Hello new article",
            url="https://www.google.com",
        )

    def test_article_content(self):
        articles = Article.objects.get(id=1)
        title = f"{articles.title}"
        description = f"{articles.description}"
        url = f"{articles.url}"

        self.assertEqual(title, "New article")
        self.assertEqual(description, "Hello new article")
        self.assertEqual(url, "https://www.google.com")

        self.assertEqual(str(articles), "New article")
