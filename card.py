from reportlab.pdfgen import canvas
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.colors import red, blue
from reportlab.lib.units import mm
from random import randint

def criar_pdf_quadrado(nome_arquivo, tamanho):
    canva = canvas.Canvas(nome_arquivo, pagesize=(tamanho, tamanho))
    table_bingo_style = TableStyle([
        ('HALIGN',(0,0),(-1,-1),'LEFT'),\
        ('GRID', (0,0), (-1,-1), 0.25, red, None, (2,2,1)), 
        ('BOX', (0,0), (-1,-1), 0.25, blue), 
    ])

    data = [
        ["B", "I", "N", "G", "O"],
    ]

    numbers_rows = []
    while len(numbers_rows) != 25:
        choosen_number = randint(1, 99)
        
        if choosen_number not in numbers_rows:
            numbers_rows.append(choosen_number)
    
    row = []
    for index, number in enumerate(numbers_rows, start=1):
        row.append(number)
        if index%5 == 0:
            data.append(row.copy())
            row.clear()

    table_bingo = Table(
        data=data,
        style=table_bingo_style,
        colWidths=100,
        rowHeights=80,
    )

    table_bingo.wrapOn(canva, tamanho, tamanho)
    table_bingo.drawOn(canva, 0, 0)
    
    canva.save()

criar_pdf_quadrado("quadrado.pdf", 500)
