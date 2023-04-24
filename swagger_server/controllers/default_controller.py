import connexion, six, os, glob, base64,zipfile, tempfile, zipfile
from swagger_server.models.images_image_id_body import ImagesImageIdBody  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server import util
from flask import jsonify, request, send_file
from datetime import datetime
from swagger_server.models.inline_response201_zip import InlineResponse201Zip
import shutil

IMAGES_FOLDER = 'images' # base folder

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER) #creation of images folder if it doesnot exists
    

def images_image_id_get(image_id):  # noqa: E501
    try:
        for extension in ALLOWED_EXTENSIONS:
            path = f'{IMAGES_FOLDER}/{image_id}.{extension}'#search in the base file 
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    image_data = f.read()
                    image_data_str = base64.b64encode(image_data).decode('utf-8')
                return jsonify({'status': 'success', 'data': image_data_str})
        
        # Search in date folders
        date_folders = sorted(os.listdir(IMAGES_FOLDER), reverse=True)
        for date_folder in date_folders:
            for extension in ALLOWED_EXTENSIONS:
                path = f'{IMAGES_FOLDER}/{date_folder}/{image_id}.{extension}'
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        image_data = f.read()
                        image_data_str = base64.b64encode(image_data).decode('utf-8')
                    return jsonify({'status': 'success', 'data': image_data_str})
                
        return jsonify({'status': 'error', 'message': 'Image not found'}), 404
    
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': 'Image not found'}), 404

def images_image_id_post(body, image_id):  # noqa: E501
    try:
        image_data = request.json['data']
        filename = request.json['filename']
        date_str = datetime.now().strftime("%d-%m-%Y")
        # Create the current date folder if it doesn't exist
        os.makedirs(os.path.join(IMAGES_FOLDER, date_str), exist_ok=True)
        # Get a list of files in the current date folder, sorted by modification time
        images_folder = os.path.abspath('images')
        date_folders = glob.glob(f"{images_folder}/*/")
        latest_date_folder = max(date_folders, key=os.path.getctime)
        image_files = glob.glob(f"{latest_date_folder}/*.jpg") + glob.glob(f"{latest_date_folder}/*.png")+glob.glob(f"{latest_date_folder}/*.jpeg") #yahan change hua hai
        files = sorted(image_files, key=os.path.getmtime)
        # If there are more than 10 files, delete the oldest ones
        if len(files) >= 10:
            for file in files[:-10]:
                os.remove(os.path.join(IMAGES_FOLDER, date_str, file))
        # Save the new image in the current date folder
        with open(os.path.join(IMAGES_FOLDER, date_str, filename), 'wb') as f:
            decoded_data = base64.b64decode(image_data)
            f.write(decoded_data)
        return jsonify({'status': 'success', 'message': 'Image uploaded', 'image_id': filename})
    except KeyError:
        return jsonify({'status': 'error', 'message': 'Invalid request data'}), 400

def images_latest_get():  # noqa: E501
    images_folder = os.path.abspath('images')
    date_folders = glob.glob(f"{images_folder}/*/")
    if not date_folders:
        return jsonify({'error': 'No images uploaded yet'}), 404
    latest_date_folder = max(date_folders, key=os.path.getctime)
    image_files = glob.glob(f"{latest_date_folder}/*.jpg") + glob.glob(f"{latest_date_folder}/*.png")+glob.glob(f"{latest_date_folder}/*.jpeg") #yahan change hua hai
    if not image_files:
        return jsonify({'error': 'No images uploaded yet'}), 404
    latest_file = max(image_files, key=os.path.getctime)
    return send_file(latest_file)


def zip_zip_id_post(file, zip_id):  # noqa: E501
    folder_name = datetime.today().strftime('%Y-%m-%d')
    path = os.path.join('images', folder_name)
    if not os.path.exists(path):
        os.makedirs(path)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    with zipfile.ZipFile(tmp_path, 'r') as zip_file:
        for name in zip_file.namelist():
            # Append a timestamp to each image filename
            filename = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + os.path.basename(name)
            with open(os.path.join(path, filename), 'wb') as f:
                f.write(zip_file.read(name))

    response = InlineResponse201Zip(
        status='success',
        message='Zip file uploaded and extracted successfully',
        zip_id=zip_id
    )
    return response, 201


def zip_get():
    # Get the list of directories in the images folder
    dirs = [d for d in os.listdir(IMAGES_FOLDER) if os.path.isdir(os.path.join(IMAGES_FOLDER, d))]

    # Sort the list of directories by creation time, in reverse order
    dirs = sorted(dirs, key=lambda x: os.path.getctime(os.path.join(IMAGES_FOLDER, x)), reverse=True)

    # Get the most recent directory
    try:
        latest_dir = dirs[0]
    except IndexError:
        return "There are no images to zip"

    # Get the list of files in the most recent directory
    files = os.listdir(os.path.join(IMAGES_FOLDER, latest_dir))

    # Sort the list of files by creation time, in reverse order
    files = sorted(files, key=lambda x: os.path.getctime(os.path.join(IMAGES_FOLDER, latest_dir, x)), reverse=True)

    # Get the first 5 files in the list
    files = files[:5]

    # Create a new zip file with a fixed name inside the images folder
    zip_file_name = "latest images.zip"
    zip_file_path = os.path.join(IMAGES_FOLDER, zip_file_name)
    zip_file = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True)

    # Add each file to the zip file
    for file in files:
        zip_file.write(os.path.join(IMAGES_FOLDER, latest_dir, file), file)

    # Close the zip file
    zip_file.close()

    # Return the zip file
    return send_file(zip_file_path, mimetype="application/zip", as_attachment=True, attachment_filename=zip_file_name)

def images_upload_post():         #mutliple post method
    if not request.is_json:
        return 'Invalid request format', 400

    images = request.json.get('images')

    if images is None or not isinstance(images, list):
        return 'No images uploaded', 400

    now = datetime.now()
    folder_name = now.strftime('%Y-%m-%d')

    folder_path = os.path.join(IMAGES_FOLDER, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for image in images:
        data = image.get('data')
        filename = image.get('filename')

        if data is None or filename is None:
            continue

        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(data))

    return 'Images uploaded successfully', 200

