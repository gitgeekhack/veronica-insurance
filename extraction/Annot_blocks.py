import os

import fitz

path = "D:/Office/veronica-self/ITC/files/new_application/"
# files = os.listdir(path)
# files = ['ITC_Dayline Duran.pdf']

for (root, dirs, file) in os.walk(path):
    for f in file:
        if '.pdf' in f:
            print(f)
            with fitz.open(os.path.join(path, f)) as doc:
                nblocks = []
                for page in doc:
                    for block in page.getText("dict")['blocks']:
                        highlight = page.addRectAnnot(block["bbox"])
                        highlight.setBlendMode(fitz.PDF_BM_Multiply)
                        highlight.update()

                doc.save(f'D:/Office/veronica-self/ITC/out/out_{f}.pdf')