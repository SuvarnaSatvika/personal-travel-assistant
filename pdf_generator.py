from fpdf import FPDF
import os

def generate_itinerary_pdf(itinerary_data: dict) -> str:
    """Takes JSON data and generates a PDF based on the AI's raw tool arguments"""

    pdf = FPDF()
    pdf.add_page()

    def clean_text(text):
        return str(text).encode('latin-1', 'replace').decode('latin-1')

    # 1. Title
    pdf.set_font("Helvetica", "B", 24)
    dest = itinerary_data.get('destination', 'Your Trip')
    pdf.cell(0, 20, clean_text(f"Trip to {dest}"), ln=True, align="C")

    days_list = itinerary_data.get("days", [])

    if isinstance(days_list, list) and len(days_list) > 0:
        for day in days_list:
            # Print Day Header
            pdf.set_font("Helvetica", "B", 14)
            day_num = day.get('day_number', '?')
            pdf.cell(0, 10, clean_text(f"Day {day_num}"), ln=True)
            
            # Print Activities
            pdf.set_font("Helvetica", "", 12)
            activities = day.get('activities', [])
            
            for act in activities:
                time = act.get('time', 'TBD')
                desc = act.get('description', 'No description')
                
                # Format:  [09:00 AM] Breakfast - @Cafe
                line = f"  [{time}] {desc}"
                pdf.multi_cell(0, 8, clean_text(line))
            
            pdf.ln(5) # Space between days
    else:
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(0, 8, "No itinerary details were found.")

    # Save and Export
    os.makedirs("exports", exist_ok=True)
    safe_dest = dest.replace(' ', '_').replace(',', '').lower()
    file_path = f"exports/itinerary_{safe_dest}.pdf"
    
    pdf.output(file_path)
    return file_path