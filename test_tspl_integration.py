#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TSPL Barcode Printer Integration - Test & Examples
Sistem entegrasyonu test etmek için örnek kodlar
"""

import requests
import json
from typing import Dict, List

class TSPLSystemTester:
    """TSPL sistem tester"""
    
    def __init__(self, base_url: str = 'http://localhost:5002', auth_token: str = None):
        """
        Initialize tester
        
        Args:
            base_url: Flask app URL
            auth_token: API token (if needed)
        """
        self.base_url = base_url
        self.session = requests.Session()
        if auth_token:
            self.session.headers.update({'Authorization': f'Bearer {auth_token}'})
    
    def check_status(self) -> Dict:
        """Check TSPL printer status"""
        try:
            response = self.session.get(f'{self.base_url}/api/tspl/status')
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def test_print(self, qr_id: str = 'TEST_QR_001', 
                  part_code: str = 'TEST', part_name: str = 'Test') -> Dict:
        """Test print a QR code"""
        try:
            response = self.session.post(
                f'{self.base_url}/api/tspl/test-print',
                json={
                    'qr_id': qr_id,
                    'part_code': part_code,
                    'part_name': part_name
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def generate_qr_with_tspl(self, part_code: str, quantity: int = 1) -> Dict:
        """Generate QR codes and print via TSPL"""
        try:
            response = self.session.post(
                f'{self.base_url}/generate_qr/{part_code}',
                json={
                    'quantity': quantity,
                    'print_to_tspl': True
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def print_batch(self, qr_ids: List[str]) -> Dict:
        """Print batch of QR codes"""
        try:
            response = self.session.post(
                f'{self.base_url}/api/tspl/print-batch',
                json={'qr_ids': qr_ids}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}


def example_1_check_printer_status():
    """Example 1: Check printer status"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Check Printer Status")
    print("="*60)
    
    tester = TSPLSystemTester()
    status = tester.check_status()
    
    print(json.dumps(status, indent=2))
    
    if status.get('connected'):
        print("✓ Printer is connected and ready!")
    else:
        print("✗ Printer is NOT connected. Check:")
        print("  - Printer IP/Port")
        print("  - Network connection")
        print("  - Printer power")


def example_2_test_print():
    """Example 2: Test print a label"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Test Print")
    print("="*60)
    
    tester = TSPLSystemTester()
    result = tester.test_print(
        qr_id='TEST_QR_001',
        part_code='Y129513-14532',
        part_name='Motor Shaft Assembly'
    )
    
    print(json.dumps(result, indent=2))
    
    if result.get('success'):
        print("✓ Test print sent successfully!")
    else:
        print(f"✗ Test print failed: {result.get('error')}")


def example_3_generate_qr_with_tspl():
    """Example 3: Generate QR codes and print via TSPL"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Generate QR + TSPL Print")
    print("="*60)
    
    tester = TSPLSystemTester()
    result = tester.generate_qr_with_tspl(
        part_code='Y129513-14532',
        quantity=5
    )
    
    print(json.dumps(result, indent=2))
    
    if result.get('success'):
        print(f"✓ Generated {len(result.get('generated', []))} QR codes")
        
        if result.get('tspl_results'):
            successful = sum(1 for r in result['tspl_results'] if r['success'])
            print(f"✓ Printed {successful}/{len(result['tspl_results'])} via TSPL")
    else:
        print(f"✗ Generation failed: {result.get('error')}")


def example_4_batch_print():
    """Example 4: Batch print multiple QR codes"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Batch Print")
    print("="*60)
    
    tester = TSPLSystemTester()
    qr_ids = [
        'Y129513-14532_1',
        'Y129513-14532_2',
        'Y129513-14532_3',
        'Y129513-14532_4',
        'Y129513-14532_5'
    ]
    
    result = tester.print_batch(qr_ids)
    
    print(json.dumps(result, indent=2))
    
    if result.get('success'):
        successful = result.get('successful', 0)
        total = result.get('total', 0)
        print(f"✓ Batch print: {successful}/{total} successful")
    else:
        print(f"✗ Batch print failed: {result.get('error')}")


def example_5_curl_requests():
    """Example 5: cURL command examples"""
    print("\n" + "="*60)
    print("EXAMPLE 5: cURL Commands")
    print("="*60)
    
    examples = [
        {
            'name': 'Check Status',
            'command': 'curl http://localhost:5002/api/tspl/status'
        },
        {
            'name': 'Test Print',
            'command': '''curl -X POST http://localhost:5002/api/tspl/test-print \\
  -H "Content-Type: application/json" \\
  -d '{"qr_id":"TEST_001","part_code":"TEST","part_name":"Test"}'
'''
        },
        {
            'name': 'Generate QR + TSPL',
            'command': '''curl -X POST http://localhost:5002/generate_qr/Y129513-14532 \\
  -H "Content-Type: application/json" \\
  -d '{"quantity":10,"print_to_tspl":true}'
'''
        },
        {
            'name': 'Batch Print',
            'command': '''curl -X POST http://localhost:5002/api/tspl/print-batch \\
  -H "Content-Type: application/json" \\
  -d '{"qr_ids":["QR_1","QR_2","QR_3"]}'
'''
        }
    ]
    
    for ex in examples:
        print(f"\n{ex['name']}:")
        print(ex['command'])


def example_6_python_integration():
    """Example 6: Python integration"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Python Integration")
    print("="*60)
    
    code = '''
from tspl_printer import TSPLManager, get_tspl_manager

# Get manager
manager = get_tspl_manager(
    printer_host='192.168.1.100',
    printer_port=9100
)

# Print single QR
success, msg = manager.print_qr_code(
    qr_id='Y129513-14532_1',
    part_code='Y129513-14532',
    part_name='Motor Shaft',
    quantity=1
)

if success:
    print(f"✓ {msg}")
else:
    print(f"✗ {msg}")

# Direct printer usage
from tspl_printer import TSPLPrinter

printer = TSPLPrinter(host='192.168.1.100', port=9100)
if printer.connect():
    printer.print_qr(
        qr_data='Y129513-14532_1',
        qr_id='Y129513-14532_1',
        part_code='Y129513-14532',
        part_name='Motor Shaft',
        quantity=5
    )
    printer.disconnect()
'''
    
    print(code)


def example_7_frontend_javascript():
    """Example 7: Frontend JavaScript integration"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Frontend JavaScript")
    print("="*60)
    
    code = '''
<!-- Load helper -->
<script src="/static/js/tspl-printer-helper.js"></script>

<script>
// Check status
await tsplPrinter.checkStatus();

// Generate QR with TSPL print
await generateQRWithTSPL('Y129513-14532', 10, true);

// Test print
await tsplPrinter.testPrint();

// Print single QR
await tsplPrinter.printQR('Y129513-14532_1', 1);

// Print batch
await tsplPrinter.printBatch([
    'Y129513-14532_1',
    'Y129513-14532_2',
    'Y129513-14532_3'
]);
</script>
'''
    
    print(code)


def example_8_configuration():
    """Example 8: Configuration setup"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Configuration Setup")
    print("="*60)
    
    config = '''
.env file settings:

# USB Printer (connected to localhost)
TSPL_PRINTER_HOST=localhost
TSPL_PRINTER_PORT=9100
TSPL_ENABLED=true

# Network Printer
TSPL_PRINTER_HOST=192.168.1.100
TSPL_PRINTER_PORT=9100
TSPL_ENABLED=true

# Disabled (PNG only)
TSPL_PRINTER_HOST=localhost
TSPL_PRINTER_PORT=9100
TSPL_ENABLED=false
'''
    
    print(config)


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " TSPL Barcode Printer Integration - Test Examples ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        example_1_check_printer_status()
        example_2_test_print()
        example_3_generate_qr_with_tspl()
        example_4_batch_print()
        example_5_curl_requests()
        example_6_python_integration()
        example_7_frontend_javascript()
        example_8_configuration()
        
        print("\n" + "="*60)
        print("✓ All examples completed!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}\n")


if __name__ == '__main__':
    # Run single example or all
    import sys
    
    if len(sys.argv) > 1:
        example = sys.argv[1]
        if example == '1':
            example_1_check_printer_status()
        elif example == '2':
            example_2_test_print()
        elif example == '3':
            example_3_generate_qr_with_tspl()
        elif example == '4':
            example_4_batch_print()
        elif example == '5':
            example_5_curl_requests()
        elif example == '6':
            example_6_python_integration()
        elif example == '7':
            example_7_frontend_javascript()
        elif example == '8':
            example_8_configuration()
        else:
            main()
    else:
        main()
