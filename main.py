from nicegui import ui
from pathlib import Path
import base64

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
        self.uploaded_image = e.content
        # Read the contents of the SpooledTemporaryFile
        self.uploaded_image.seek(0)  # Ensure we're at the beginning of the file
        image_bytes = self.uploaded_image.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        self.image_container.set_source(f'data:image/png;base64,{image_base64}')
        ui.notify('Image uploaded successfully!', type='positive')

    def clear_image(self):
        self.uploaded_image = None
        self.image_container.set_source('./placeholder.png')
        self.file_picker.reset()
        ui.notify('Image cleared')

    def get_image(self):
        return self.uploaded_image

# Usage example
def main():
    ui.query('body').classes('bg-gray-100')

    # Add viewport meta tag for proper mobile rendering
    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">')

    # Add custom CSS for mobile optimization
    ui.add_head_html('''
        <style>
        body {
            font-size: 16px;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }
        </style>
    ''')

    uploader = ImageUploader()
    uploader.create()

    def handle_submit():
        image = uploader.get_image()
        if image:
            # Process the image here
            ui.notify('Processing image...', type='info')
        else:
            ui.notify('Please upload an image first', type='warning')

    ui.button('Submit', on_click=handle_submit).classes('mt-4 w-full')


main()
ui.run(title="Image Uploader", favicon="📷")