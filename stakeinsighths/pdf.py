from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Create PDF path
pdf_path = "/Users/varunrana/Desktop/Madhu_Rani_Teacher_CV.pdf"


# Create the canvas
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# Helper for line height and margins
x_margin = 50
y = height - 50
line_height = 14

def draw_line(text, bold=False):
    global y
    if y < 60:
        c.showPage()
        y = height - 50
    if bold:
        c.setFont("Helvetica-Bold", 10)
    else:
        c.setFont("Helvetica", 10)
    c.drawString(x_margin, y, text)
    y -= line_height

# Header
c.setFont("Helvetica-Bold", 16)
c.drawString(x_margin, y, "Madhu Rani")
y -= 20

c.setFont("Helvetica", 10)
c.drawString(x_margin, y, "Teacher | Noida, India | madhurani4april@gmail.com | 9354349026")
y -= 25

# Sections
c.setFont("Helvetica-Bold", 12)
c.drawString(x_margin, y, "Professional Summary")
y -= 16
draw_line("Driven educator with experience at Noida Public School, adept in Lesson Planning and Student Mentoring.")
draw_line("Demonstrated success in Curriculum Implementation and fostering motivational environments.")
draw_line("Proven track record in enhancing student learning outcomes through innovative teaching methods.")
draw_line("Excels in collaborative settings, committed to continual professional development.")
y -= 10

c.setFont("Helvetica-Bold", 12)
c.drawString(x_margin, y, "Work Experience")
y -= 16

draw_line("PRT Teacher – Noida Public School (04/2022 - 12/2024)", bold=True)
draw_line("- Documented student work to exhibit and celebrate learning.")
draw_line("- Communicated with parents about student progress and concerns.")
draw_line("- Collaborated with colleagues to develop stimulating curriculum.")
y -= 8

draw_line("TGT Teacher – Noida International Public School (04/2009 - 03/2021)", bold=True)
draw_line("- Skilled at working independently and in team environments.")
draw_line("- Provided support and guidance to peers and students.")
draw_line("- Committed to learning and continual professional improvement.")
y -= 10

c.setFont("Helvetica-Bold", 12)
c.drawString(x_margin, y, "Education")
y -= 16
draw_line("- Master of Arts (English, Hindi) – JV Jain College, Saharanpur")
draw_line("- B.Ed – JV Jain College, Saharanpur")
draw_line("- BA – MD University, Rohtak")
y -= 10

c.setFont("Helvetica-Bold", 12)
c.drawString(x_margin, y, "Skills")
y -= 16
draw_line("Lesson Planning | Student Mentoring | Curriculum Implementation | Classroom Management")
draw_line("Progress Reporting | Motivational Abilities")
y -= 10

c.setFont("Helvetica-Bold", 12)
c.drawString(x_margin, y, "Languages")
y -= 16
draw_line("Hindi – Full Professional Proficiency")
draw_line("English – Full Professional Proficiency")
y -= 10

c.setFont("Helvetica-Bold", 12)
c.drawString(x_margin, y, "Interests")
y -= 16
draw_line("Reading | Cooking")

# Save the PDF
c.save()
pdf_path
