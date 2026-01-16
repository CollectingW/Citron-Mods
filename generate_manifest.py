import os
import json

def generate_manifest():
    manifest = {}
    # '.' means it looks in the same folder where the script is located
    base_dir = "." 

    # 1. Look for Title ID folders
    for tid in os.listdir(base_dir):
        if not os.path.isdir(tid) or tid.startswith('.'): 
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
                
                # 4. Check if it's an exefs or romfs mod
                is_exefs = os.path.exists(os.path.join(mod_path, "exefs"))
                is_romfs = os.path.exists(os.path.join(mod_path, "romfs"))
                
                mod_type = "exefs" if is_exefs else "romfs"
                
                # Find the actual patch files (e.g., 2.0.0.pchtxt)
                type_folder = "exefs" if is_exefs else "romfs"
                final_path = os.path.join(mod_path, type_folder)
                files = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f))]

                manifest[tid]["versions"][version]["patches"].append({
                    "name": mod_name,
                    "type": mod_type,
                    "files": files,
                    "rel_path": f"{tid}/{version}/{mod_name}/{type_folder}"
                })

    # Save the manifest
    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)
    
    print("✅ Success! manifest.json has been created.")
    print(f"Detected {len(manifest)} games in the repo.")

if __name__ == "__main__":
    generate_manifest()
