import os
import logging
from pypdf import PdfWriter

# Suppress pypdf logging warnings (removes "Object 2 0 not defined")
logging.getLogger("pypdf").setLevel(logging.ERROR)

# Configuration
SOURCE_DIR = "source"
MERGED_DIR = "merged"

def setup_directories(base_dir="."):
    """Ensure that the source and merged directories exist."""
    source_path = os.path.join(base_dir, SOURCE_DIR)
    merged_path = os.path.join(base_dir, MERGED_DIR)
    
    if not os.path.exists(source_path):
        os.makedirs(source_path)
        print(f"Created folder '{SOURCE_DIR}' at: {os.path.abspath(source_path)}")
        
    if not os.path.exists(merged_path):
        os.makedirs(merged_path)
        print(f"Created folder '{MERGED_DIR}' at: {os.path.abspath(merged_path)}")
        
    return source_path, merged_path

def merge_pdf_groups():
    """
    Merges all PDF files grouped by prefix 'N' from the source folder.
    Example: N-1.pdf, N-2.pdf, N-3.pdf -> N.pdf
    """
    source_path, merged_path = setup_directories()
    
    print("-" * 30)
    print(f"Searching for files in: {os.path.abspath(source_path)}")
    print(f"Output will be saved to: {os.path.abspath(merged_path)}\n")

    try:
        all_files = os.listdir(source_path)
    except FileNotFoundError:
        print(f"Error: Folder '{SOURCE_DIR}' not found.")
        return

    pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
    groups_to_merge = {}

    for filename in pdf_files:
        try:
            parts = filename.split('-')
            if len(parts) >= 2:
                group_id_str = parts[0]
                sub_number_part = parts[1].split('.')[0]
                
                # Keep group_id as string to handle non-numeric prefixes, 
                # but sort sub-numbers as integers.
                sub_number = int(sub_number_part)
                
                if group_id_str not in groups_to_merge:
                    groups_to_merge[group_id_str] = {}
                
                groups_to_merge[group_id_str][sub_number] = filename
        except (ValueError, IndexError):
            continue

    if not groups_to_merge:
        print("No PDF files found with the 'N-Number.pdf' format.")
        return

    # Sort group IDs (handles 1, 2, 10 correctly if they are numeric strings)
    sorted_groups = sorted(groups_to_merge.keys(), key=lambda x: int(x) if x.isdigit() else x)
    total_merged_groups = 0
    
    for group_id in sorted_groups:
        sub_files_dict = groups_to_merge[group_id]
        sorted_subs = sorted(sub_files_dict.keys())
        
        if len(sorted_subs) < 2:
            print(f"⚠️  Skipping group '{group_id}': Only 1 file found.")
            continue

        output_filename = os.path.join(merged_path, f"{group_id}.pdf")
        merger = PdfWriter()
        files_added = []

        try:
            for sub in sorted_subs:
                filename = sub_files_dict[sub]
                merger.append(os.path.join(source_path, filename))
                files_added.append(filename)
            
            with open(output_filename, "wb") as output_file:
                merger.write(output_file)
            
            print(f"✅ Merged {len(files_added)} files -> {group_id}.pdf")
            total_merged_groups += 1
                
        except Exception as e:
            print(f"❌ Failed to merge group '{group_id}': {e}")
        finally:
            merger.close()
    
    print("-" * 30)
    print(f"\nProcess Complete! {total_merged_groups} groups merged into '{MERGED_DIR}'.")

if __name__ == "__main__":
    merge_pdf_groups()