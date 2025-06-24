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



import io
import os
from datetime import datetime
from decimal import Decimal

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont # For custom fonts if needed, otherwise Helvetica/Times are default

# Assuming settings is available from Django context
# from django.conf import settings 

def generate_order_pdf(order):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()

    # Define custom paragraph styles for better typography
    styles.add(ParagraphStyle(name='HeadingAgriKart',
                               fontName='Helvetica-Bold',
                               fontSize=28,
                               leading=32,
                               alignment=1, # TA_CENTER
                               textColor=colors.HexColor('#2e7d32') # Primary Green
                               ))
    styles.add(ParagraphStyle(name='SubHeading',
                               fontName='Helvetica-Bold',
                               fontSize=16,
                               leading=20,
                               alignment=1, # TA_CENTER
                               textColor=colors.HexColor('#333333')
                               ))
    styles.add(ParagraphStyle(name='SectionTitle',
                               fontName='Helvetica-Bold',
                               fontSize=12,
                               leading=14,
                               textColor=colors.HexColor('#1b5e20'), # Secondary Green
                               spaceAfter=6
                               ))
    styles.add(ParagraphStyle(name='NormalText',
                               fontName='Helvetica',
                               fontSize=10,
                               leading=14,
                               textColor=colors.HexColor('#333333')
                               ))
    styles.add(ParagraphStyle(name='SmallText',
                               fontName='Helvetica',
                               fontSize=8,
                               leading=10,
                               textColor=colors.HexColor('#666666')
                               ))
    styles.add(ParagraphStyle(name='BoldText',
                               fontName='Helvetica-Bold',
                               fontSize=10,
                               leading=14,
                               textColor=colors.HexColor('#333333')
                               ))
    styles.add(ParagraphStyle(name='TotalAmount',
                               fontName='Helvetica-Bold',
                               fontSize=12,
                               leading=16,
                               textColor=colors.HexColor('#2e7d32')
                               ))
    styles.add(ParagraphStyle(name='Guidelines',
                               fontName='Helvetica',
                               fontSize=8,
                               leading=11,
                               textColor=colors.HexColor('#333333')
                               ))
    styles.add(ParagraphStyle(name='FooterText',
                               fontName='Helvetica-Oblique',
                               fontSize=7,
                               leading=9,
                               alignment=1, # TA_CENTER
                               textColor=colors.gray
                               ))

    Story = []
    width, height = A4 # Get page dimensions for calculations if needed


    # --- Header Section ---
    # Attempt to load logo dynamically (assuming settings.BASE_DIR points to project root)
    # For a real deployment, make sure static files are collected and accessible.
    logo_path = 'static/logo/agrikart-logo.png' # Example path, adjust as needed.
                                              # You might need to pass settings.BASE_DIR explicitly
                                              # or configure ReportLab's image search path.
    # Placeholder if logo not found (or remove if logo is mandatory)
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=0.95 * inch, height=0.8 * inch) # Adjust size
        logo.hAlign = 'LEFT'
    else:
        logo = Paragraph("", styles['NormalText']) # Empty placeholder

    header_data = [[logo, Paragraph("<b>AgriKart.ai</b>", styles['HeadingAgriKart'])]]
    header_table = Table(header_data, colWidths=[1.5*inch, None])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    Story.append(header_table)
    Story.append(Spacer(1, 0.2 * inch)) # Space after header

    Story.append(Paragraph(f"Order Summary - #{order.id}", styles['SubHeading']))
    Story.append(Spacer(1, 0.2 * inch))

    # --- Order Info Block ---
    order_info_data = [
        [Paragraph("<b>Order Placed:</b>", styles['BoldText']), Paragraph(order.created_at.strftime('%B %d, %Y %I:%M %p'), styles['NormalText'])],
        [Paragraph("<b>Order ID:</b>", styles['BoldText']), Paragraph(f"#{order.id}", styles['NormalText'])],
        [Paragraph("<b>Payment Status:</b>", styles['BoldText']), Paragraph('Success' or 'N/A', styles['NormalText'])], # Assuming payment_status
        [Paragraph("<b>Overall Status:</b>", styles['BoldText']), Paragraph(order.status or 'N/A', styles['NormalText'])], # Assuming order status
    ]
    order_info_table = Table(order_info_data, colWidths=[1.5*inch, None])
    order_info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'LEFT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    Story.append(order_info_table)
    Story.append(Spacer(1, 0.2 * inch))

    # --- Shipping Details ---
    Story.append(Paragraph("Shipping Details", styles['SectionTitle']))
    shipping_details_data = [
        [Paragraph("<b>Buyer Name:</b>", styles['BoldText']), Paragraph(order.buyer.user.username if order.buyer and order.buyer.user else 'N/A', styles['NormalText'])],
        [Paragraph("<b>Buyer Phone:</b>", styles['BoldText']), Paragraph(order.buyer.user.phone_number if order.buyer and order.buyer.user else 'N/A', styles['NormalText'])],
        [Paragraph("<b>Delivery Address:</b>", styles['BoldText']), Paragraph(order.buyer.address or 'N/A', styles['NormalText'])],
        [Paragraph("<b>Shipping Speed:</b>", styles['BoldText']), Paragraph("Same-day Farm Pickup", styles['NormalText'])],
    ]
    shipping_details_table = Table(shipping_details_data, colWidths=[1.7*inch, None])
    shipping_details_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    Story.append(shipping_details_table)
    Story.append(Spacer(1, 0.3 * inch))


    # --- Items Ordered ---
    Story.append(Paragraph("Items Ordered", styles['SectionTitle']))
    
    item_header_data = [
        Paragraph("<b>Product Name</b>", styles['BoldText']),
        Paragraph("<b>Quantity</b>", styles['BoldText']),
        Paragraph("<b>Unit Price</b>", styles['BoldText']),
        Paragraph("<b>Subtotal</b>", styles['BoldText'])
    ]
    items_data = [item_header_data]

    subtotal_items = Decimal("0.00")
    for item in order.items.all():
        item_price = Decimal(str(item.produce.price)) # Convert to Decimal for safe calculation
        item_quantity = Decimal(str(item.quantity))
        item_total = item_price * item_quantity
        subtotal_items += item_total
        items_data.append([
            Paragraph(item.produce.name, styles['NormalText']),
            Paragraph(f"{item.quantity} {item.produce.unit if hasattr(item.produce, 'unit') and item.produce.unit else ''}", styles['NormalText']), # Assuming produce has a 'unit' attribute
            Paragraph(f"₹{item_price:.2f}", styles['NormalText']),
            Paragraph(f"₹{item_total:.2f}", styles['NormalText'])
        ])

    item_table = Table(items_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.5*inch]) # Adjust column widths
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e9f5e9')), # Header background
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1b5e20')), # Header text color
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'), # Align price/subtotal to right
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('TOPPADDING', (0,0), (-1,0), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e0e0e0')), # Light grid lines
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cccccc')), # Outer box
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fcfcfc')]), # Zebra striping
    ]))
    Story.append(item_table)
    Story.append(Spacer(1, 0.3 * inch))


    # --- Payment Summary ---
    Story.append(Paragraph("Payment Summary", styles['SectionTitle']))

    # Use actual order.total_amount if available, otherwise calculate
    # It's better to trust the backend's calculated total_amount if present
    # Assuming order.total_amount, order.shipping_cost, order.tax_amount are fields on the Order model
    # If not, use the previous logic with fixed values or calculate.
    shipping = Decimal(str(order.shipping_cost)) if hasattr(order, 'shipping_cost') and order.shipping_cost is not None else Decimal("0.00")
    tax = Decimal(str(order.tax_amount)) if hasattr(order, 'tax_amount') and order.tax_amount is not None else Decimal("0.00")
    grand_total = Decimal(str(order.total_amount)) if hasattr(order, 'total_amount') and order.total_amount is not None else (subtotal_items + shipping + tax)

    payment_summary_data = [
        [Paragraph("Item(s) Subtotal:", styles['NormalText']), Paragraph(f"₹{subtotal_items:.2f}", styles['NormalText'])],
        [Paragraph("Shipping Charges:", styles['NormalText']), Paragraph(f"₹{shipping:.2f}", styles['NormalText'])],
        [Paragraph("Estimated Tax:", styles['NormalText']), Paragraph(f"₹{tax:.2f}", styles['NormalText'])],
        [Paragraph("<b>Grand Total:</b>", styles['TotalAmount']), Paragraph(f"<b>₹{grand_total:.2f}</b>", styles['TotalAmount'])],
    ]
    payment_summary_table = Table(payment_summary_data, colWidths=[None, 1.5*inch]) # Right column fixed width
    payment_summary_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'), # Align amounts to right
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (0,-2), (-1,-2), 1, colors.HexColor('#cccccc')), # Line above total
        ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
        ('TOPPADDING', (0,-1), (-1,-1), 10),
    ]))
    Story.append(payment_summary_table)
    Story.append(Spacer(1, 0.4 * inch))


    # --- Buyer Guidelines ---
    Story.append(Paragraph("Buyer Policy and Guidelines", styles['SectionTitle']))
    Story.append(Spacer(1, 0.1 * inch))

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
        Story.append(Paragraph(rule, styles['Guidelines']))
        Story.append(Spacer(1, 0.05 * inch)) # Small space between rules

    Story.append(Spacer(1, 0.4 * inch))

    Story.append(Paragraph("For full legal terms, refer to agrikart.com/legal or contact our support.", styles['FooterText']))


    # Build the PDF
    doc.build(Story)
    buffer.seek(0)
    return buffer