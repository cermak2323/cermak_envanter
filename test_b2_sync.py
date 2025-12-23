#!/usr/bin/env python3
"""
B2 File Sync Test Script
Tüm kategorileri test eder
"""

from b2_file_sync import B2FileSyncManager

def main():
    print("\n" + "="*70)
    print("B2 FILE SYNC TEST")
    print("="*70 + "\n")
    
    manager = B2FileSyncManager()
    
    print("\n1. Durum Kontrolü")
    print("-" * 70)
    
    for category in manager.SYNC_CATEGORIES.keys():
        print(f"\n[{category.upper()}]")
        
        local_files = manager.get_local_files(category)
        b2_files = manager.get_b2_files(category)
        
        local_paths = {f['path'] for f in local_files}
        b2_paths = {f['path'] for f in b2_files}
        
        missing_in_b2 = local_paths - b2_paths
        missing_locally = b2_paths - local_paths
        
        print(f"  Lokal Dosya:       {len(local_files)}")
        print(f"  B2 Dosya:          {len(b2_files)}")
        print(f"  B2'de Eksik:       {len(missing_in_b2)}")
        print(f"  Lokalde Eksik:     {len(missing_locally)}")
        print(f"  Senkronize:        {len(local_paths & b2_paths)}")
        
        if missing_in_b2:
            print(f"\n  B2'ye yüklenecek ilk 5 dosya:")
            for path in list(missing_in_b2)[:5]:
                print(f"    - {path}")
        
        if missing_locally:
            print(f"\n  Lokale indirilecek ilk 5 dosya:")
            for path in list(missing_locally)[:5]:
                print(f"    - {path}")
    
    print("\n" + "="*70)
    print("\nTest tamamlandı!")
    print("\nSenkronizasyon için:")
    print("  python b2_file_sync.py sync_all")
    print("  python b2_file_sync.py sync qr_codes")
    print("  python b2_file_sync.py upload reports")
    print("  python b2_file_sync.py download part_photos")
    print()

if __name__ == '__main__':
    main()
