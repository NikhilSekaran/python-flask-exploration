import os
import zipfile
import tempfile

based_dir = os.path.abspath(os.path.dirname(__file__))

variant_info_folder_path = os.path.join(based_dir, 'ACP20017')
lead_info_folder_path = os.path.join(based_dir, 'ACP29001')


def write_to_zip(file_path, folder, zip_fp):
    for root_path, dir_name, files in os.walk(file_path):
        for file in files:
            if file not in ['conaninfo.txt', 'conanmanifest.txt']:
                abs_file_path = os.path.join(root_path, file)
                if file_path != root_path:
                    temp = root_path.split(file_path)
                    folder_name = folder + temp[1]
                    folder_path = os.path.join(folder_name, file)
                else:
                    folder_path = os.path.join(folder, file)
                zip_fp.write(filename=abs_file_path, arcname=folder_path)


def create_download_package():
    zip_handler = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    zip_fp = zipfile.ZipFile(zip_handler, 'w', zipfile.ZIP_DEFLATED)
    write_to_zip(variant_info_folder_path, '20017_Output', zip_fp)
    write_to_zip(lead_info_folder_path, '29001_Output', zip_fp)

    zip_fp.close()
    zip_handler.close()
    return zip_handler.name


if __name__ == '__main__':
    # create package
    zip_file_path = create_download_package()
    print(f'zip_file_path: {zip_file_path}')