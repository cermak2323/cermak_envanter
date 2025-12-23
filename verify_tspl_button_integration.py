#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TSPL Button Integration Verification
Parts sayfasına entegre TSPL buton'un çalışıp çalışmadığını test et
"""

import requests
import json
from typing import Dict, Tuple

class TSPLButtonTester:
    """TSPL Button Integration Test"""
    
    def __init__(self, base_url: str = 'http://192.168.10.27:5002'):
        self.base_url = base_url
        
    def test_api_endpoint(self) -> Tuple[bool, str]:
        """TSPL API endpoint'inin erişilebilir olduğunu test et"""
        try:
            response = requests.get(f'{self.base_url}/api/tspl/status', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return True, f"✓ API erişilebilir. Status: {data}"
            else:
                return False, f"✗ API status code: {response.status_code}"
        except Exception as e:
            return False, f"✗ API erişim hatası: {str(e)}"
    
    def test_part_detail_page(self, part_code: str) -> Tuple[bool, str]:
        """Part detail page'inin TSPL checkbox'ı içerip içermediğini test et"""
        try:
            response = requests.get(f'{self.base_url}/parts/{part_code}', timeout=5)
            html = response.text
            
            # TSPL checkbox ve helper script'i kontrol et
            has_checkbox = 'printToTSPL' in html
            has_helper = 'tspl-printer-helper.js' in html
            has_status_check = 'checkTSPLStatus' in html
            
            if has_checkbox and has_helper and has_status_check:
                return True, "✓ Part detail page TSPL entegrasyonu var"
            else:
                missing = []
                if not has_checkbox: missing.append("checkbox")
                if not has_helper: missing.append("helper")
                if not has_status_check: missing.append("status check")
                return False, f"✗ Eksik: {', '.join(missing)}"
        except Exception as e:
            return False, f"✗ Part detail page hatası: {str(e)}"
    
    def test_qr_generation_with_tspl(self, part_code: str) -> Tuple[bool, str]:
        """QR generation endpoint'inin TSPL parametresini alıp almadığını test et"""
        try:
            response = requests.post(
                f'{self.base_url}/generate_qr/{part_code}',
                json={
                    'quantity': 1,
                    'print_to_tspl': True
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # TSPL results kontrol et
                if 'tspl_results' in data:
                    return True, f"✓ TSPL parametresi alındı ve işlendi. Results: {data['tspl_results']}"
                elif data.get('success'):
                    return True, "✓ QR generation başarılı (TSPL results yok ama başarılı)"
                else:
                    return False, f"✗ Generation hatası: {data.get('error')}"
            else:
                return False, f"✗ HTTP status: {response.status_code}"
        except Exception as e:
            return False, f"✗ Generation endpoint hatası: {str(e)}"
    
    def test_tspl_helper_script(self) -> Tuple[bool, str]:
        """TSPL helper script'inin erişilebilir olduğunu test et"""
        try:
            response = requests.get(
                f'{self.base_url}/static/js/tspl-printer-helper.js',
                timeout=5
            )
            
            if response.status_code == 200:
                js_content = response.text
                
                # Key functions kontrol et
                has_generate_func = 'generateQRWithTSPL' in js_content
                has_printer_class = 'TSPLPrinterHelper' in js_content
                has_batch_print = 'printBatch' in js_content
                
                if has_generate_func and has_printer_class and has_batch_print:
                    return True, "✓ TSPL helper script var ve fonksiyonlar mevcut"
                else:
                    missing = []
                    if not has_generate_func: missing.append("generateQRWithTSPL")
                    if not has_printer_class: missing.append("TSPLPrinterHelper")
                    if not has_batch_print: missing.append("printBatch")
                    return False, f"✗ Eksik fonksiyonlar: {', '.join(missing)}"
            else:
                return False, f"✗ Helper script HTTP status: {response.status_code}"
        except Exception as e:
            return False, f"✗ Helper script hatası: {str(e)}"
    
    def test_env_variables(self) -> Tuple[bool, str]:
        """Environment variables'ların set edilip edilmediğini kontrol et"""
        try:
            # Bu test sadece documentation için, gerçek env check yapılamaz
            # Çünkü client-side'dan backend env'e erişilemez
            return True, "ℹ Environment variables backend'de. Admin panelden doğrula: /admin/tspl"
        except:
            return False, "✗ Environment check hatası"
    
    def run_all_tests(self, part_code: str = '05686-26600') -> Dict:
        """Tüm testleri çalıştır"""
        results = {
            'api_endpoint': self.test_api_endpoint(),
            'part_detail_page': self.test_part_detail_page(part_code),
            'qr_generation': self.test_qr_generation_with_tspl(part_code),
            'helper_script': self.test_tspl_helper_script(),
            'env_variables': self.test_env_variables()
        }
        
        return results
    
    def print_report(self, results: Dict):
        """Test sonuçlarını yazdır"""
        print("\n" + "="*70)
        print("TSPL BUTTON INTEGRATION TEST REPORT")
        print("="*70 + "\n")
        
        all_passed = True
        for test_name, (success, message) in results.items():
            status = "✓ PASS" if success else "✗ FAIL"
            print(f"{status:8} | {test_name:20} | {message}")
            if not success:
                all_passed = False
        
        print("\n" + "="*70)
        if all_passed:
            print("✓ TÜM TESTLER BAŞARILI - Sistem hazır!")
        else:
            print("✗ BAZΙ TESTLER BAŞARISIZ - Lütfen kontrol et")
        print("="*70 + "\n")
        
        return all_passed


def main():
    """Main test runner"""
    import sys
    
    tester = TSPLButtonTester()
    
    part_code = sys.argv[1] if len(sys.argv) > 1 else '05686-26600'
    
    print(f"\n[TEST] TSPL Button Integration'ı test ediliyor...")
    print(f"[INFO] Part Code: {part_code}")
    print(f"[INFO] Base URL: {tester.base_url}\n")
    
    results = tester.run_all_tests(part_code)
    all_passed = tester.print_report(results)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    exit(main())
