from django.core.management.base import BaseCommand
import cv2
import os
from django.conf import settings
from myapp.models import User

class Command(BaseCommand):
    help = 'Register a user face for authentication'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email')
        parser.add_argument('image_path', type=str, help='Path to face image')

    def handle(self, *args, **options):
        try:
            # Get user by email
            user = User.objects.get(email=options['email'])
            print(f"Found user: {user.email} (ID: {user.id})")
            
            # Read the image
            img = cv2.imread(options['image_path'])
            if img is None:
                self.stdout.write(self.style.ERROR(f'Could not read image: {options["image_path"]}'))
                return
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                self.stdout.write(self.style.ERROR('No face detected in the image'))
                return
                
            if len(faces) > 1:
                self.stdout.write(self.style.ERROR('Multiple faces detected in the image'))
                return
            
            # Get the face ROI
            (x, y, w, h) = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            
            # Resize to standard size
            face_roi = cv2.resize(face_roi, (150, 150))
            
            # Save the face image
            face_dir = os.path.join(settings.MEDIA_ROOT, 'face_auth')
            os.makedirs(face_dir, exist_ok=True)
            
            face_path = os.path.join(face_dir, f'{user.id}.jpg')
            cv2.imwrite(face_path, face_roi)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully registered face for user {user.email}\n'
                    f'User ID: {user.id}\n'
                    f'Face saved at: {face_path}'
                )
            )
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found with the provided email'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
