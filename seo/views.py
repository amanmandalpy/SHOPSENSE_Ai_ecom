from django.http import HttpResponse

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Disallow: /sys/",
        "Disallow: /dashboard/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def sitemap_xml(request):
    # This is a basic stub, for a real production site you'd use django.contrib.sitemaps
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{request.build_absolute_uri('/')}</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{request.build_absolute_uri('/products/')}</loc>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>
</urlset>"""
    return HttpResponse(xml, content_type="application/xml")
