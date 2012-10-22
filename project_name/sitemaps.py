from django.contrib.sitemaps import Sitemap


class StaticSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return [
            '/',
        ]

    def location(self, obj):
        return obj
