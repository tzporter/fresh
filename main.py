import json
from nicegui import ui
from pathlib import Path
import base64
from PIL import Image
import io
from together2 import generate_json


image_base64 = None
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
        global image_base64
        image_base64 = base64.b64encode(self.image_bytes).decode('utf-8')
        self.image_container.set_source(f'data:image/png;base64,{image_base64}')

        
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
        with open('items.json', 'r') as f:
            entries = json.load(f)
        with ui.column().classes('w-full h-screen pb-8'):
            for entry in entries:
                display_fruit_data(json.dumps(entry))
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
        # image = Image.open(io.BytesIO(self.image_bytes))
        # image.save("images/image.png")
        # ui.notify("test")
        
        # image = self.uploader.get_image()
        if self.uploader.image_bytes is not None:
            ui.navigate.to('/submit')
            
        else:
            ui.notify('Please upload an image first', type='warning')

class SubmitPage:
    def __init__(self):
        self.page = ui.page('/submit')
        ui.label('Image Submission').classes('text-xl font-bold mb-2')
        ui.image().classes('w-full h-48 object-contain mt-4').set_source(f'data:image/png;base64,{image_base64}')

        fruit_json_str = generate_json(image_base64)
        # ui.textarea(value=fruit_json_str)
        # fruit_json = json.loads(fruit_json_str)

        display_fruit_data(fruit_json_str.strip(), save=True)

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



def display_fruit_data(json_data, save=False):
    # Parse the JSON data
    try:
        entry = json.loads(json_data)
        if save:
            with open('items.json', 'r') as f:
                entries = json.load(f)
                # ui.notify(entries)
            entries.append(entry)
            with open('items.json', 'w') as f:
                json.dump(entries, f)
        data = entry
    except:
        ui.notify(f'Invalid JSON data: {json_data}', type='error')
        return
    
    # Create a card to display the information
    with ui.column().classes('w-full h-full items-center justify-center'):

        with ui.card().classes('w-full p-4'):
            ui.label(f"{data['emoji']} {data['item'].capitalize()} {data['emoji']}").classes('text-xl font-bold mb-2')
            
            with ui.row().classes('justify-between mb-2'):
                ui.label('Quantity:')
                ui.label(f"{data['quantity']}")
            ui.label('•'*data['quantity'] ).classes('mb-1').style(f'font-weight: bold; font-size: 4em; margin-bottom: -.5em; margin-top: -1em;')

            
            days_left = data['time-left']
            if days_left > 3:
                color = 'green'
            elif days_left > 1:
                color = 'orange'
            else:
                color = 'red'
            with ui.row().classes('justify-between mb-2'):
                ui.label('Time Left:').classes('mb-1')
                ui.label(f"{days_left} day{'s' if days_left != 1 else ''} left").classes('text-sm text-gray-600').style(f'color: {color};')
            ui.label('•'*days_left ).classes('mb-1').style(f'color: {color}; font-weight: bold; font-size: 4em; margin-bottom: -.5em; margin-top: -1em;')

            ripeness = data['ripeness']
            if ripeness > 6:
                color = 'green'
            elif ripeness > 3:
                color = 'orange'
            else:
                color = 'red'
            with ui.row().classes('justify-between mb-2'):
                ui.label('Ripeness:').classes('mb-1')
                ui.label(f"{ripeness} / 10").classes('text-sm text-gray-600').style(f'color: {color};')
            with ui.row().classes('justify-between mb-2'):
                ui.label('•'*ripeness ).classes('mb-1').style(f'color: {color}; font-weight: bold; font-size: 4em; margin: -1em 0 -.5em 0;')
                # ui.label('•'*(10-ripeness) ).classes('mb-1').style(f'color: grey; font-weight: bold; font-size: 4em; margin: -1em -.em -.5em 0;')

