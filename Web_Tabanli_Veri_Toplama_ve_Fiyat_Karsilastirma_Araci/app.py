from flask import Flask, render_template_string, request, send_file
from bs4 import BeautifulSoup
import pandas as pd
import io

from web import get_dynamic_html_content, parse_trendyol, process_data

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Trendyol Fiyat Karşılaştırma</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #f9f9f9, #ececec);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            margin-top: 50px;
            max-width: 900px;
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0px 6px 18px rgba(0,0,0,0.1);
        }
        .btn-custom {
            background: #ff6f00;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        .btn-custom:hover {
            background: #e65100;
            transform: scale(1.05);
        }
        h1 { font-weight: bold; color: #333; }
        table { margin-top: 20px; }
        th { background: #ff6f00; color: white; text-align: center; }
        td { text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center"> Trendyol Fiyat Karşılaştırma</h1>
        <p class="text-muted text-center">Ürün linkini gir, fiyatları tablo halinde gör ve CSV olarak indir.</p>
        <form method="POST" class="mt-4">
            <div class="input-group">
                <input type="text" name="url" class="form-control form-control-lg" placeholder="https://www.trendyol.com/..." required>
                <button type="submit" class="btn btn-custom">Verileri Getir</button>
            </div>
        </form>

        {% if table %}
            <hr>
            <h3> Sonuçlar</h3>
            <div class="table-responsive">
                {{ table|safe }}
            </div>
            <form method="POST" action="/download">
                <input type="hidden" name="url" value="{{ url }}">
                <button type="submit" class="btn btn-success mt-3"> CSV İndir</button>
            </form>
        {% endif %}
    </div>
</body>
</html>
"""

# Bellekte son dataframe'i saklamak için
last_df = None

@app.route("/", methods=["GET", "POST"])
def index():
    global last_df
    table_html = None
    url = None

    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "⚠️ Lütfen bir URL girin."

        html_content = get_dynamic_html_content(url)
        if not html_content:
            return "❌ Sayfa yüklenemedi."

        soup = BeautifulSoup(html_content, "html.parser")
        scraped_data = parse_trendyol(soup)
        if not scraped_data:
            return "❌ Satıcı bilgisi bulunamadı."

        df = process_data(scraped_data)
        last_df = df  # belleğe al
        table_html = df.to_html(classes="table table-bordered table-striped", index=False)

    return render_template_string(HTML_PAGE, table=table_html, url=url)


@app.route("/download", methods=["POST"])
def download():
    global last_df
    if last_df is None:
        return "❌ İndirilecek veri yok."

    output = io.BytesIO()
    last_df.to_csv(output, index=False, encoding="utf-8-sig")
    output.seek(0)
    return send_file(output,
                     as_attachment=True,
                     download_name="urunler.csv",
                     mimetype="text/csv")


if __name__ == "__main__":
    app.run(debug=True)
