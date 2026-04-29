import json
import os

def build_manifest(search_dirs=['assets', 'data'], output_file='metadata_manifest.json'):
    manifest = []
    
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
            
        # Walk through the directory
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                # Only look for .json files that aren't the manifest itself or schemas
                if file.endswith('.json') and file != output_file and 'schemas' not in root:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            
                            # Add relative path to the primary asset file
                            if 'files' in data:
                                # For images
                                if 'image' in data['files']:
                                    image_path = os.path.join(root, data['files']['image'])
                                    data['files']['relative_path'] = image_path
                                # For data files
                                elif 'main' in data['files']:
                                    main_path = os.path.join(root, data['files']['main'])
                                    data['files']['relative_path'] = main_path
                            
                            manifest.append(data)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    # Write the combined manifest to the root
    with open(output_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Successfully built manifest with {len(manifest)} entries at {output_file}")

if __name__ == "__main__":
    build_manifest()
