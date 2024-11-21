from django.core.mail import EmailMessage
from io import BytesIO
from reportlab.pdfgen import canvas


def generate_invoice(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, f"Invoice for Order ID: {order.order_id}")
    p.drawString(100, 730, f"Total Amount: {order.total_price}")
    p.drawString(100, 710, f"Status: {order.status}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def send_invoice_email(order):
    invoice_pdf = generate_invoice(order)
    email = EmailMessage(
        subject=f"Invoice for Order {order.order_id}",
        body="Please find your invoice attached.",
        from_email="noreply@yourstore.com",
        to=[order.user.email],
    )
    email.attach(f"Invoice_{order.order_id}.pdf", invoice_pdf.read(), 'application/pdf')
    email.send()
