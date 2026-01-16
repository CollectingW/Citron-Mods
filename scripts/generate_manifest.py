import os
import json

def generate_manifest():
    manifest = {}
    # Folders to skip
    ignore = ['.git', '.github', 'scripts', 'README.md', 'manifest.json', '.gitkeep']

    # 1. Walk Title ID folders
    for tid in os.listdir('.'):
        if tid in ignore or not os.path.isdir(tid):
            continue
        
        manifest[tid] = {"versions": {}}
        tid_path = os.path.join('.', tid)
        
        # 2. Walk Version folders (e.g., 1.0.0)
        for version in os.listdir(tid_path):
            v_path = os.path.join(tid_path, version)
            if not os.path.isdir(v_path):
                continue
            
            manifest[tid]["versions"][version] = {"patches": []}
            
            # 3. Walk Mod Name folders (e.g., Moon Jump)
            for mod_name in os.listdir(v_path):
                mod_path = os.path.join(v_path, mod_name)
                if not os.path.isdir(mod_path):
                    continue
                
                # 4. Grab EVERY subfolder inside the Mod folder (exefs, cheats, etc.)
                for sub_folder in os.listdir(mod_path):
                    final_path = os.path.join(mod_path, sub_folder)
                    if not os.path.isdir(final_path):
                        continue
                        
                    # Get the files inside (e.g., the .txt or .pchtxt)
                    files = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f))]
                    
                    if files:
                        # Create an entry for the manifest
                        manifest[tid]["versions"][version]["patches"].append({
                            "name": mod_name,
                            "type": sub_folder, # This will be 'cheats', 'exefs', etc.
                            "files": files,
                            "rel_path": f"{tid}/{version}/{mod_name}/{sub_folder}"
                        })

    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)
    
    print("Manifest updated. All mod types (cheats/exefs/romfs) included.")

if __name__ == "__main__":
    generate_manifest()
