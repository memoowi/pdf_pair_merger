import os
from pypdf import PdfWriter

# Tentukan nama folder input dan output
SOURCE_DIR = "source"
MERGED_DIR = "merged"

def setup_directories(base_dir="."):
    """Memastikan folder source dan merged sudah ada."""
    
    source_path = os.path.join(base_dir, SOURCE_DIR)
    merged_path = os.path.join(base_dir, MERGED_DIR)
    
    if not os.path.exists(source_path):
        os.makedirs(source_path)
        print(f"Folder '{SOURCE_DIR}' made in: {os.path.abspath(source_path)}")
        
    if not os.path.exists(merged_path):
        os.makedirs(merged_path)
        print(f"Folder '{MERGED_DIR}' made in: {os.path.abspath(merged_path)}")
        
    return source_path, merged_path


def merge_pdf_pairs_by_folder():
    """
    Menggabungkan file PDF berpasangan dari folder 'source' dan
    menyimpan hasilnya di folder 'merged'.
    """
    
    source_path, merged_path = setup_directories()
    
    print("-" * 30)
    print(f"Seaching files in: {os.path.abspath(source_path)}")
    print(f"Output will be saved in: {os.path.abspath(merged_path)}\n")

    # Kumpulkan semua nama file PDF yang ada di folder 'source'
    try:
        all_files = os.listdir(source_path)
    except FileNotFoundError:
        print(f"Error: Folder '{SOURCE_DIR}' not found.")
        return

    pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
    
    pairs_to_merge = {}

    for filename in pdf_files:
        try:
            parts = filename.split('-')
            
            if len(parts) == 2 and parts[1].lower().endswith('.pdf'):
                N = int(parts[0])
                sub_number_str = parts[1].split('.')[0]
                sub_number = int(sub_number_str)
                
                if sub_number == 1 or sub_number == 2:
                    if N not in pairs_to_merge:
                        pairs_to_merge[N] = {}
                    
                    pairs_to_merge[N][sub_number] = filename
                    
        except ValueError:
            continue

    
    if not pairs_to_merge:
        print("No PDF file pairs in 'N-1.pdf' and 'N-2.pdf' formats were found in 'source' folder.")
        return

    sorted_N = sorted(pairs_to_merge.keys())
    total_merged = 0
    
    for N in sorted_N:
        pair = pairs_to_merge[N]
        
        file1 = pair.get(1)
        file2 = pair.get(2)
        
        output_filename = os.path.join(merged_path, f"{N}.pdf")
        
        if file1 and file2:
            print(f"Merging {file1} and {file2} -> {N}.pdf")
            
            merger = PdfWriter()
            
            try:
                # Path lengkap ke file sumber
                path_file1 = os.path.join(source_path, file1)
                path_file2 = os.path.join(source_path, file2)
                
                merger.append(path_file1)
                merger.append(path_file2)
                
                # Tulis hasil gabungan ke folder 'merged'
                with open(output_filename, "wb") as output_file:
                    merger.write(output_file)
                
                total_merged += 1
                
            except Exception as e:
                print(f"Failed to merge pairs for {N}. Error: {e}")
                
            finally:
                merger.close()
                
        else:
            missing_file = file1 if file1 else file2
            if missing_file:
                print(f"⚠️ Skipping file: {missing_file}. Pair is incomplete.")
    
    print("-" * 30)
    print(f"\n✅ Process finished. Total {total_merged} pairs merged successfully to '{MERGED_DIR}'.")

if __name__ == "__main__":
    merge_pdf_pairs_by_folder()