import json
import os

def build_manifest(assets_dir='assets', output_file='metadata_manifest.json'):
    manifest = []
    
    # Walk through the assets directory
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            # Only look for .json files that aren't .gitkeep or the manifest itself
            if file.endswith('.json') and file != output_file:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        # Add relative path to the image from the manifest location
                        # This assumes the 'file' field in JSON is just the filename
                        # We might want to make it relative to the root for the manifest
                        
                        # Calculate path relative to project root for the asset file
                        # root is something like 'assets/economics/money'
                        if 'files' in data and 'image' in data['files']:
                            image_path = os.path.join(root, data['files']['image'])
                            data['files']['relative_image_path'] = image_path
                        
                        manifest.append(data)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Write the combined manifest to the root
    with open(output_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Successfully built manifest with {len(manifest)} entries at {output_file}")

if __name__ == "__main__":
    build_manifest()
