# logistics/utils.py

from geopy.distance import geodesic
from logistics.models import CourierAssignment, LogisticsPartner
import math
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.lib.units import inch
from reportlab.lib import colors
from decimal import Decimal
import io
import os
from decimal import Decimal
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.conf import settings

def assign_order_to_courier(order):
    if not (order.farmer_lat and order.farmer_lon):
        print("❌ Order missing farmer coordinates")
        return

    courier_candidates = LogisticsPartner.objects.all()
    farmer_location = (order.farmer_lat, order.farmer_lon)

    for courier in courier_candidates:
        courier_location = (courier.latitude, courier.longitude)
        distance = geodesic(farmer_location, courier_location).km

        if distance <= 15:
            CourierAssignment.objects.create(
                courier=courier,
                order=order,
                distance_km=distance
            )
            print(f"✅ Assigned courier {courier.name} to order {order.id}")
            return

    print("🚫 No suitable courier found within 15km")




def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the distance in kilometers between two points on the Earth using the haversine formula.
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    radius = 6371  # Radius of earth in kilometers
    return c * radius



def generate_order_pdf(order):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x_margin = 40
    y = height - 50

    # 🌾 AgriKart Header
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.green)
    c.drawCentredString(width / 2, y, "🌾 AgriKart")
    c.setFillColor(colors.black)
    y -= 35

    # Optional: logo image
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'logo', 'agrikart-logo.png')
    if os.path.exists(logo_path):
        c.drawImage(logo_path, x_margin, y, width=70, height=40, preserveAspectRatio=True)
    y -= 50

    # Order Summary Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, f"Order Summary - #{order.id}")
    y -= 25

    # Order Info
    c.setFont("Helvetica", 10)
    c.drawString(x_margin, y, f"Order Placed: {order.created_at.strftime('%B %d, %Y')}")
    y -= 15
    c.drawString(x_margin, y, f"Order ID: #{order.id}")
    y -= 15

    # Subtotal calc
    subtotal = Decimal("0.00")
    for item in order.items.all():
        subtotal += item.produce.price * item.quantity

    shipping = Decimal("0.00")
    tax = Decimal("0.00")
    total = subtotal + shipping + tax

    c.drawString(x_margin, y, f"Total Amount: ₹{total:.2f}")
    y -= 25

    # Shipping Info
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.darkgreen)
    c.drawString(x_margin, y, "Shipping Details")
    c.setFillColor(colors.black)
    y -= 15

    c.setFont("Helvetica", 10)
    c.drawString(x_margin, y, f"Buyer Address: {order.buyer.address or 'N/A'}")
    y -= 15
    c.drawString(x_margin, y, "Shipping Speed: Same-day Farm Pickup")
    y -= 25

    # Items
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Items Ordered")
    y -= 15
    c.line(x_margin, y, width - x_margin, y)
    y -= 10

    c.setFont("Helvetica", 10)
    for item in order.items.all():
        c.drawString(x_margin, y, f"{item.produce.name} × {item.quantity}")
        c.drawRightString(width - x_margin, y, f"₹{item.produce.price * item.quantity:.2f}")
        y -= 15

    y -= 25

    # Payment Summary
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Payment Summary")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(x_margin, y, "Item(s) Subtotal:")
    c.drawRightString(width - x_margin, y, f"₹{subtotal:.2f}")
    y -= 15
    c.drawString(x_margin, y, "Shipping:")
    c.drawRightString(width - x_margin, y, f"₹{shipping:.2f}")
    y -= 15
    c.drawString(x_margin, y, "Estimated Tax:")
    c.drawRightString(width - x_margin, y, f"₹{tax:.2f}")
    y -= 15
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_margin, y, "Grand Total:")
    c.drawRightString(width - x_margin, y, f"₹{total:.2f}")
    y -= 30

    # ✅ Buyer Guidelines
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x_margin, y, "Buyer Policy and Guidelines")
    y -= 15
    c.setFont("Helvetica", 9)

    guidelines = [
        "1. All sales are final for perishable goods unless physical damage is documented at delivery.",
        "2. Cancellation requests must be submitted within 15 minutes of order placement.",
        "3. Delivery shall be attempted twice; unavailability of the recipient may result in cancellation.",
        "4. Refunds for canceled orders (if eligible) will be processed within 48 business hours.",
        "5. AgriKart is not liable for delays due to unforeseen logistical or environmental conditions.",
        "6. Buyers are responsible for ensuring correct address and contact details during checkout.",
        "7. AgriKart reserves the right to modify pricing, availability, or delivery estimates at its discretion.",
        "8. By placing an order, the buyer agrees to comply with these terms and acknowledges the nature of agricultural perishables.",
    ]

    for rule in guidelines:
        c.drawString(x_margin, y, rule)
        y -= 13
        if y < 100:  # paginate
            c.showPage()
            y = height - 60
            c.setFont("Helvetica", 9)

    # Footer
    y -= 20
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.gray)
    c.drawCentredString(width / 2, y, "For full legal terms, refer to agrikart.com/legal or contact our support.")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

