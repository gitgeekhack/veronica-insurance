from app.manage import create_app
from app.resource.pdf_extractor.PDFExtractor import HomePage, DataExtraction

app, logger = create_app()

app.router.add_view('/', HomePage, name="home")
app.router.add_view('/extract', DataExtraction, name="search")

