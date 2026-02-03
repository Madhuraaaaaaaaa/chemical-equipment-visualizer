from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import EquipmentDataset
import pandas as pd

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO


@api_view(['POST'])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    df = pd.read_csv(file)

    summary = {
        "total_count": int(len(df)),
        "avg_flowrate": float(df["Flowrate"].mean()),
        "avg_pressure": float(df["Pressure"].mean()),
        "avg_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict()
    }

    EquipmentDataset.objects.create(
        name=file.name,
        summary=summary
    )

    # keep only last 5
    if EquipmentDataset.objects.count() > 5:
        EquipmentDataset.objects.first().delete()

    return Response(summary)


@api_view(['GET'])
def latest_summary(request):
    last = EquipmentDataset.objects.last()
    if not last:
        return Response({"message": "No data uploaded yet"})
    return Response(last.summary)


@api_view(['GET'])
def history(request):
    data = EquipmentDataset.objects.order_by('-upload_time')[:5]
    result = []
    for d in data:
        result.append({
            "name": d.name,
            "upload_time": d.upload_time,
            "summary": d.summary
        })
    return Response(result)


@api_view(['GET'])
def generate_pdf(request):
    last = EquipmentDataset.objects.last()
    if not last:
        return Response({"message": "No data available"})

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)

    y = 800
    p.drawString(100, y, "Chemical Equipment Dataset Report")
    y -= 30
    p.drawString(100, y, f"Dataset: {last.name}")
    y -= 20
    p.drawString(100, y, f"Uploaded: {last.upload_time}")
    y -= 30

    for key, value in last.summary.items():
        if key == "type_distribution":
            p.drawString(100, y, "Type Distribution:")
            y -= 20
            for k, v in value.items():
                p.drawString(120, y, f"{k}: {v}")
                y -= 15
        else:
            p.drawString(100, y, f"{key}: {value}")
            y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')
