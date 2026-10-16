
from celery import shared_task
from .models import AuctionImage
from .fashion_prediction import predict_auction_category


@shared_task
def predict_auction_category_task(prediction_id):
    try:
        uploaded_image = AuctionImage.objects.get(id=prediction_id)
        uploaded_image.status = 'PROCESSING'
        uploaded_image.save(update_fields=['status'])

        result = predict_auction_category(uploaded_image.image.path)

        category = result.get('category')
        confidence = result.get('confidence')

        if not category or confidence is None:
            raise ValueError("Unable to predict the category.")

        uploaded_image.predicted_category = str(category)
        uploaded_image.confidence = float(confidence)
        uploaded_image.status = 'COMPLETED'
        uploaded_image.save(update_fields=[
            'predicted_category',
            'confidence',
            'status'
        ])

    except Exception:
        AuctionImage.objects.filter(id=prediction_id).update(status='FAILED')
