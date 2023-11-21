import sys
import os
from pathlib import Path
import re
import shutil

FORBIDDEN_DIRS = []
documents = []
documents_ext = []
images = []
images_ext = []
video = []
video_ext = []
audio = []
audio_ext = []
archives = []
archives_ext = []
dont_now = []
dont_now_ext = []

categories = {
    'images': ('.jpeg', '.png', '.jpg', '.svg'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.xlsx', '.pptx', '.pdf'),
    'archives': ('.zip', '.tar', '.gz'),
    'audio': ('.mp3', '.wav', '.ogg', '.amr'),
    'dont_now_ext': ()
}

translit_dict = {
    ord('а'): 'a', ord('б'): 'b', ord('в'): 'v', ord('г'): 'h', 
    ord('ґ'): 'g', ord('д'): 'd', ord('е'): 'e', ord('є'): 'ie', 
    ord('ж'): 'zh', ord('з'): 'z', ord('и'): 'y', ord('і'): 'i', 
    ord('ї'): 'i', ord('й'): 'i', ord('к'): 'k', ord('л'): 'l', 
    ord('м'): 'm', ord('н'): 'n', ord('о'): 'o', ord('п'): 'p',
    ord('р'): 'r', ord('с'): 's', ord('т'): 't', ord('у'): 'u', 
    ord('ф'): 'f', ord('х'): 'kh', ord('ц'): 'ts', ord('ч'): 'ch', 
    ord('ш'): 'sh', ord('щ'): 'shch', ord('ь'): '', ord('ю'): 'iu', 
    ord('я'): 'ia', ord('А'): 'A', ord('Б'): 'B', ord('В'): 'V', 
    ord('Г'): 'H', ord('Ґ'): 'G', ord('Д'): 'D', ord('Е'): 'E', 
    ord('Є'): 'Ye', ord('Ж'): 'Zh', ord('З'): 'Z', ord('И'): 'Y', 
    ord('І'): 'I', ord('Ї'): 'Yi', ord('Й'): 'Y', ord('К'): 'K', 
    ord('Л'): 'L', ord('М'): 'M', ord('Н'): 'N', ord('О'): 'O', 
    ord('П'): 'P', ord('Р'): 'R', ord('С'): 'S', ord('Т'): 'T', 
    ord('У'): 'U', ord('Ф'): 'F', ord('Ч'): 'Kh', ord('Ц'): 'Ts', 
    ord('Ч'): 'Ch', ord('Ш'): 'Sh', ord('Щ'): 'Shch', ord('Ь'): '', 
    ord('Ю'): 'Yu', ord('Я'): 'Ya', ord('ы'): 'y', ord('ъ'): ''
}

def normalize(file_name):

    translate_name = file_name.translate(translit_dict)
    result_name = re.sub(r'(?!\.)\W', '_', translate_name)
    return result_name

def move_files(path):

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_name = normalize(file)
            new_file_path = os.path.join(root, new_file_name)
            os.rename(file_path, new_file_path)
            shutil.move(new_file_path, os.path.join(path, new_file_name))
        for dir in dirs:
            move_files(os.path.join(root, dir))

def remove_empty_folders(path):

    walk = list(os.walk(path))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0 and path not in FORBIDDEN_DIRS:
            os.rmdir(path)


def sort_files(path):

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            ext = os.path.splitext(file)[1]
            if ext.lower() in categories['documents']:
                documents.append(file)
                documents_ext.append(ext.lower())
                file_path = os.path.join(path, 'documents')
                shutil.move(os.path.join(path, file), os.path.join(file_path, file))
            elif ext.lower() in categories['images']:
                images.append(file)
                images_ext.append(ext.lower())
                file_path = os.path.join(path, 'images')
                shutil.move(os.path.join(path, file), os.path.join(file_path, file))
            elif ext.lower() in categories['video']:
                video.append(file)
                video_ext.append(ext.lower())
                file_path = os.path.join(path, 'video')
                shutil.move(os.path.join(path, file), os.path.join(file_path, file))
            elif ext.lower() in categories['audio']:
                audio.append(file)
                audio_ext.append(ext.lower())
                file_path = os.path.join(path, 'audio')
                shutil.move(os.path.join(path, file), os.path.join(file_path, file))        
            elif ext.lower() in categories['archives']:
                archives.append(file)
                archives_ext.append(ext.lower())
                file_path = os.path.join(path, 'archives')
                shutil.move(os.path.join(path, file), os.path.join(file_path, file))
                archive_path = os.path.join(file_path, os.path.splitext(file)[0])
                os.makedirs(archive_path, exist_ok=True)
                try:
                    shutil.unpack_archive(os.path.join(file_path, file), archive_path)
                except shutil.ReadError as err:
                    print(f"Не вдалося розархівувати файл {archive_path}: {err}")                    
            else:
                dont_now.append(file)
                dont_now_ext.append(ext.lower())
                file_path = os.path.join(path, 'dont_now_ext')
                shutil.move(os.path.join(path, file), os.path.join(file_path, file))

    print(f'***********З В І Т  про  Р Е З У Л Ь Т А Т И  роботи  С К Р И П Т А ********')
    print(f'Список файлів в категорії - Документи: \n{documents}')
    print(f'та розширення файлів документів: \n{set(documents_ext)}')
    print(f'Список файлів в категорії - Фото: \n{images}')
    print(f'та розширення фотофайлів: \n{set(images_ext)}')
    print(f'Список файлів в категорії - Відео: \n{video}')
    print(f'та розширення видеофайлів: \n{set(video_ext)}')
    print(f'Список файлів в категорії - Аудіо: \n{audio}')
    print(f'та розширення аудіофайлів: {set(audio_ext)}')
    print(f'Список файлів в категорії - Архиви: \n{archives}')
    print(f'та розширення архивів: \n{set(archives_ext)}')
    print(f'Список файлів в категорії - Файли з невідомим розширенням: \n{dont_now}')
    print(f'та їх розширення, які невідомі Скрипту: \n{set(dont_now_ext)}')
    print(f'Всі відомі Скрипту розширення знайдені ним у цільовій папці: \n{set(documents_ext)^set(images_ext)^set(video_ext)^set(audio_ext)^set(archives_ext)}')
    print(f'Дякую за увагу та допомогу!!!')


def main():

    try:
        if len(sys.argv) != 2:
            print(f'Usage: {sys.argv[0]} Pyth - Перевірте правильність вводу даних')
            sys.exit(1)
        list_dir = Path(sys.argv[1])
        if list_dir.is_dir():
            for category in categories:
                category_path = os.path.join(list_dir, category)
                os.makedirs(category_path, exist_ok=True)
                FORBIDDEN_DIRS.append(category_path)
    except UnboundLocalError:
            print(f'Usage: {sys.argv[0]} Pyth ')
            sys.exit(1)

        
    move_files(list_dir)

    sort_files(list_dir)

    remove_empty_folders(list_dir)

if __name__ == "__main__":
    main()
