import os
import json

def generate_manifest():
    manifest = {}
    base_dir = "." 
    
    # Folders to ignore
    ignore = ['.git', '.github', 'scripts', 'README.md', 'manifest.json']

    # 1. Look for Title ID folders
    for tid in os.listdir(base_dir):
        if tid in ignore or not os.path.isdir(tid):
            continue
        
        manifest[tid] = {"versions": {}}
        
        # 2. Look for Version folders (e.g., 2.0.0)
        tid_path = os.path.join(base_dir, tid)
        for version in os.listdir(tid_path):
            version_path = os.path.join(tid_path, version)
            if not os.path.isdir(version_path):
                continue
            
            manifest[tid]["versions"][version] = {"patches": []}
            
            # 3. Look for Mod Name folders (e.g., 21.9 Ultrawide)
            for mod_name in os.listdir(version_path):
                mod_path = os.path.join(version_path, mod_name)
                if not os.path.isdir(mod_path):
                    continue
                
                # 4. Check for exefs or romfs
                is_exefs = os.path.exists(os.path.join(mod_path, "exefs"))
                is_romfs = os.path.exists(os.path.join(mod_path, "romfs"))
                
                if not (is_exefs or is_romfs):
                    continue

                type_folder = "exefs" if is_exefs else "romfs"
                final_path = os.path.join(mod_path, type_folder)
                
                # Get all files inside the exefs/romfs folder
                files = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f))]

                manifest[tid]["versions"][version]["patches"].append({
                    "name": mod_name,
                    "type": type_folder,
                    "files": files,
                    "rel_path": f"{tid}/{version}/{mod_name}/{type_folder}"
                })

    # Save the manifest at the root
    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)
    
    print("Manifest updated successfully.")

if __name__ == "__main__":
    generate_manifest()
