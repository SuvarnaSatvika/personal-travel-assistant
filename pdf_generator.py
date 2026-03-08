from fpdf import FPDF
import os

def generate_itinerary_pdf(itinerary_data: dict) -> str:
    """Takes JSON data and generates a PDF"""

    pdf = FPDF()
    pdf.add_page()

    #Title
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0,20, f"Trip to {itinerary_data.get('destination', 'unknown')}", ln=True, align="C")

    #Subtitle
    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 10, "Your Travel itinerary is here", ln=True, align="C")
    pdf.ln(10)

    #Day-wise itinerary
    if "itinerary" in itinerary_data and itinerary_data["itinerary"]:
        pdf.set_font("Helvetica" , "B", 16)
        pdf.cell(0,10, "Daily Plan", ln=True)
        pdf.set_font("Helvetica", "", 12)

        for day_plan in itinerary_data["itinerary"]:
            pdf.multi_cell(0,8,f"{day_plan}")
            pdf.ln(2)
        pdf.ln(5)
    #Events
    if "events" in itinerary_data:
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0,10,"Events", ln=True)
        pdf.set_font("Helvetica", "", 12)

        for event in itinerary_data["events"]:
            pdf.cell(0,8,f"-{event.get('name')} at {event.get('venue')}", ln=True)
            pdf.set_text_color(100,100,100)
            pdf.cell(0,6,f" Date: {event.get('date')} | Time: {event.get('time', 'TBD')}", ln=True)
            pdf.set_text_color(0,0,0)

    os.makedirs("exports", exist_ok=True)
    file_path = f"exports/itinerary_{itinerary_data.get('destination', 'trip').lower()}.pdf"
    pdf.output(file_path)

    return file_path