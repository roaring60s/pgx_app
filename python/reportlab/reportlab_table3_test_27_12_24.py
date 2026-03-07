from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
import csv

TSV1 = "/media/p/D11/patients/01_report_template/report_lab/table3_test_reportUX.txt"
PDF1 = "/media/p/D11/patients/01_report_template/report_lab/pdf_output1B.pdf"


def generate_pdf_from_tsv(tsv_file, pdf_file):
	"""
	Generates a PDF file from a TSV file, creating a table with custom row colors,
	centered text, a paragraph before the table, and repeating headers.
	
	Args:
		tsv_file: Path to the input TSV file.
		pdf_file: Path to the output PDF file.
	"""
	data = []
	row_colors = []
	
	with open(tsv_file, 'r') as file:
		reader = csv.reader(file, delimiter='\t')
		header = next(reader)  # Read the header row
		data.append(header[:5])  # Add header to data
		
		for row in reader:
			data.append(row[:5])  # Take the first 5 columns
			try:
				rgb_str = row[6]  # 7th column for RGB
				r, g, b = map(int, rgb_str.split(','))
				row_colors.append(colors.Color(r / 255.0, g / 255.0, b / 255.0))
			except (IndexError, ValueError):
				row_colors.append(colors.white)  # Default to white if color is invalid
	
	doc = SimpleDocTemplate(pdf_file, pagesize=letter)
	styles = getSampleStyleSheet()
	
	# Add a paragraph before the table
	lorem_ipsum_text = "lorem ipsum, lorem ipsum, lorem ipsum, lorem ipsum, lorem ipsum, lorem ipsum, lorem ipsum"
	paragraph_style = ParagraphStyle(name='LoremStyle', alignment=TA_CENTER)  # Center align the paragraph
	paragraph = Paragraph(lorem_ipsum_text, paragraph_style)
	
	# Create table with repeating header
	table = Table(data, repeatRows=1)
	
	# Apply table style
	table_style = TableStyle([
		('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
		('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
		('ALIGN', (0, 0), (-1, -1), 'CENTER'),
		('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment to CENTER
		('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
		('BOTTOMPADDING', (0, 0), (-1, 0), 12),
		('GRID', (0, 0), (-1, -1), 1, colors.black)
	])
	
	# Apply row colors
	for i, color in enumerate(row_colors):
		table_style.add('BACKGROUND', (0, i + 1), (-1, i + 1), color)  # +1 to skip header row
	
	table.setStyle(table_style)
	
	elements = []
	elements.append(paragraph)
	
	# Add 2 blank rows (Spacers) after the paragraph
	elements.append(Spacer(1, 0.2 * inch))  # 0.2 inches of space
	elements.append(Spacer(1, 0.2 * inch))  # 0.2 inches of space
	
	elements.append(table)
	doc.build(elements)


generate_pdf_from_tsv(TSV1, PDF1)

print(f"PDF file '{PDF1}' created successfully.")
