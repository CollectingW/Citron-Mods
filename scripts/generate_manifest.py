import os
import json

def generate_manifest():
    manifest = {}
    base_dir = "." 
    
    ignore = ['.git', '.github', 'scripts', 'README.md', 'manifest.json']

    for tid in os.listdir(base_dir):
        if tid in ignore or not os.path.isdir(tid):
            continue
        
        manifest[tid] = {"versions": {}}
        
        tid_path = os.path.join(base_dir, tid)
        for version in os.listdir(tid_path):
            version_path = os.path.join(tid_path, version)
            if not os.path.isdir(version_path):
                continue
            
            manifest[tid]["versions"][version] = {"patches": []}
            
            for mod_name in os.listdir(version_path):
                mod_path = os.path.join(version_path, mod_name)
                if not os.path.isdir(mod_path):
                    continue
                
                # Check for all three valid mod subfolders
                is_exefs = os.path.exists(os.path.join(mod_path, "exefs"))
                is_romfs = os.path.exists(os.path.join(mod_path, "romfs"))
                is_cheats = os.path.exists(os.path.join(mod_path, "cheats"))
                
                # If it doesn't have any of these, it's not a mod folder we want
                if not (is_exefs or is_romfs or is_cheats):
                    continue

                # Determine the folder type to download
                if is_exefs:
                    type_folder = "exefs"
                elif is_romfs:
                    type_folder = "romfs"
                else:
                    type_folder = "cheats"

                final_path = os.path.join(mod_path, type_folder)
                files = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f))]

                manifest[tid]["versions"][version]["patches"].append({
                    "name": mod_name,
                    "type": type_folder,
                    "files": files,
                    "rel_path": f"{tid}/{version}/{mod_name}/{type_folder}"
                })

    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)
    
    print("Manifest updated successfully including cheats support.")

if __name__ == "__main__":
    generate_manifest()
