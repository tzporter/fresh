from nicegui import ui
from pathlib import Path
import base64
from PIL import Image
import io



class ImageUploader:
    def __init__(self):
        self.uploaded_image = None
        self.image_container = None

    def create(self):
        with ui.card().classes('w-full max-w-sm mx-auto'):
            ui.label('Upload Image').classes('text-xl font-bold mb-2')
            
            with ui.row().classes('w-full items-center justify-center'):
                self.file_picker = ui.upload(
                    label='Choose file',
                    auto_upload=True,
                    max_file_size=5_000_000,  # 5 MB
                    on_upload=self.handle_upload,
                ).props('accept=image/*').classes('w-full')

            self.image_container = ui.image().classes('w-full h-48 object-contain mt-4')
            self.image_container.set_source('')  # Set a placeholder image

            with ui.row().classes('w-full justify-end'):
                ui.button('Clear', on_click=self.clear_image).classes('mt-2')

    def handle_upload(self, e):

        uploaded_image = e.content
        uploaded_image.seek(0)
        self.image_bytes = uploaded_image.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        self.image_container.set_source(f'data:image/png;base64,{image_base64}')

        image = Image.open(io.BytesIO(image_bytes))
        image.save("image.png")
        ui.notify('Image uploaded successfully!', type='positive')

    def clear_image(self):
        self.uploaded_image = None
        self.image_container.set_source('./placeholder.png')
        self.file_picker.reset()
        ui.notify('Image cleared')

    def get_image(self):
        return self.uploaded_image

class HomePage:
    def __init__(self):
        self.page = ui.page('/home')
        with ui.column().classes('w-full h-screen pb-8'):
            ui.label('').classes('flex-grow')
            with ui.row().classes('w-full justify-center items-center'):
                ui.button('Button 1', on_click=lambda: ui.navigate.to('/home')).classes('mx-2')
                ui.button('+', on_click=lambda: ui.navigate.to('/upload')).classes('mx-2 rounded-full w-12 h-12')
                ui.button('Button 2', on_click=lambda: ui.navigate.to('/home')).classes('mx-2')

class UploadPage:
    def __init__(self):
        self.page = ui.page('/upload')
        self.uploader = ImageUploader()
        self.uploader.create()
        ui.button('Submit', on_click=self.handle_submit).classes('mt-4 w-full')
        ui.button('Back to Home', on_click=lambda: ui.navigate.to('/home')).classes('mt-4 w-full')

    def handle_submit(self):
        image = self.uploader.get_image()
        if image:
            ui.navigate.to('/submit')
        else:
            ui.notify('Please upload an image first', type='warning')

class SubmitPage:
    def __init__(self):
        self.page = ui.page('/submit')
        
        ui.label('Image Submission').classes('text-xl font-bold mb-2')
        ui.button('Back to Home', on_click=lambda: ui.navigate.to('/home')).classes('mt-4 w-full')

def main():
    ui.query('body').classes('bg-gray-100')

    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">')

    ui.add_head_html('''
        <style>
        body {
            font-size: 16px;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }
        </style>
    ''')

    ui.page('/home')(HomePage)
    ui.page('/upload')(UploadPage)
    ui.page('/submit')(SubmitPage)

    ui.navigate.to('/home')

    ui.run(title="Image Uploader", favicon="📷")

if __name__ in {"__main__", "__mp_main__"}:
    main()
