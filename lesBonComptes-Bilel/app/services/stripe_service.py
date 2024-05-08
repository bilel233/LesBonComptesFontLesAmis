
from werkzeug.utils import secure_filename
from ..models.payment_info import PaymentInfo
from flask import current_app
import os

def save_payment_method(user, payment_method, rib_file=None):
    payment_info = PaymentInfo(user=user, payment_method=payment_method)
    if rib_file:
        # Sauvegarder le fichier RIB dans un dossier sécurisé
        rib_filename = secure_filename(rib_file.filename)
        rib_path = os.path.join(current_app.config['UPLOAD_FOLDER'], rib_filename)
        rib_file.save(rib_path)
        payment_info.rib_file.put(rib_file, content_type=rib_file.content_type, filename=rib_filename)
    payment_info.save()
    return payment_info
