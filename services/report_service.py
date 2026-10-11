import database
from reportlab.pdfgen import canvas
from functions import get_result_by_id
from pathlib import Path
# set variable equal to the path for reports folder
REPORT_DIR = Path(__file__).parent / "reports"
# make report folder if it does not exist
REPORT_DIR.mkdir(exist_ok=True)
# dictionary
fields = [
    ("Detection ID", "id"),
    ("Species", "species"),
    ("Filename", "filename"),
    ("Confidence", "confidence")
]
# TODO: edit this for the live version to have it as a download option or something. can practice on local version
# function that will create pdf with data. passed the ID from the frontend based on what generate report button is pressed
def generate_report(detection_id):
    detection = get_result_by_id(detection_id) # set the varible to the actual place in the database

    if detection is None: #if it isnt a real entry then do nothing 
        return

    pdf_path = REPORT_DIR / f"report_{detection_id}.pdf" 

    pdf = canvas.Canvas(str(pdf_path)) # create pdf and set font for header
    pdf.setFont("Times-Roman", 18)
    pdf.drawString(100, 750, "ImmersaVLM Detection Report")

    y = 700
    pdf.setFont("Helvetica", 12)

    for label, key in fields:
        pdf.drawString(100, y, f"{label}: {detection[key]}")
        y -= 20
    # get spectogram
    image_path = (
        Path(__file__).parent
        / "spectrograms"
        / detection["filename"].replace(".wav", ".jpg")
    )
    # test for image path working
    #print("IMAGE PATH:", image_path)
    #print("IMAGE EXISTS:", image_path.exists())
    # set image size 
    pdf.drawImage(
        str(image_path),
        100,
        300,
        width=400,
        height=250,
        preserveAspectRatio=True
    )
    # save pdf on system
    pdf.save()
    # print complete message
    print("PDF CREATED:", pdf_path)
