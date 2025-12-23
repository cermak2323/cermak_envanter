# Parts Info - Code Changes Reference

## Quick Navigation

- [Database Columns](#database-columns)
- [API Changes](#api-changes)
- [Frontend Changes](#frontend-changes)
- [Warning System](#warning-system)

---

## Database Columns

### New Columns Created

```sql
-- In update_parts_info_columns() function
ALTER TABLE parts_info ADD COLUMN replacement_code VARCHAR(100);
ALTER TABLE parts_info ADD COLUMN build_out TINYINT(1) DEFAULT 0;
```

### Schema Definition
```python
# app.py, line 1440-1444
new_columns = [
    ('stock_location', 'VARCHAR(255)'),
    ('machines', 'TEXT'),
    ('specifications', 'TEXT'),
    ('replacement_code', 'VARCHAR(100)'),  # Değişen parça kodu
    ('build_out', 'TINYINT(1) DEFAULT 0')  # BUILD OUT bayrağı
]
```

---

## API Changes

### GET /api/parts_info/get_all

**Before** (10 columns selected):
```python
cursor.execute('''
    SELECT 
        part_code, part_name, stock, critical_stock, expected_stock,
        supplier, purchase_price_eur, description, sale_price_eur, photo_path
    FROM parts_info
    ORDER BY part_code
''')
```

**After** (12 columns selected):
```python
cursor.execute('''
    SELECT 
        part_code, part_name, stock, critical_stock, expected_stock,
        supplier, purchase_price_eur, description, sale_price_eur, 
        photo_path, replacement_code, build_out
    FROM parts_info
    ORDER BY part_code
''')
```

**Response - Before**:
```python
part = {
    'part_code': row[0],
    'part_name': row[1],
    'stock': row[2],
    'supplier': row[5],
    'purchase_price_eur': float(row[6]),
    'description': row[7],
    'sale_price_eur': float(row[8]),
    'photo_path': row[9]
}
```

**Response - After**:
```python
part = {
    'part_code': row[0],
    'part_name': row[1],
    'stock': row[2],
    'supplier': row[5],
    'purchase_price_eur': float(row[6]),
    'description': row[7],
    'sale_price_eur': float(row[8]),
    'photo_path': row[9],
    'replacement_code': row[10] or '',      # ← NEW
    'build_out': bool(row[11]) if row[11] else False  # ← NEW
}
```

---

## Frontend Changes

### HTML - Table Headers

**Before** (main.html, line 626-635):
```html
<div class="parts-list-header">
    <div>Parça Kodu</div>
    <div>Parça İsmi</div>
    <div>Stok Durumu</div>
    <div>Tedarikçi</div>
    <div>Kullanıldığı Makineler</div>
</div>
```

**After** (main.html, line 626-637):
```html
<div class="parts-list-header">
    <div>Parça Kodu</div>
    <div>Parça Adı</div>
    <div>Stok</div>
    <div>Tedarikçi</div>
    <div>Geliş (€)</div>
    <div>Tanım</div>
    <div>Satış (€)</div>
    <div>Değişen Kod</div>
    <div>BUILD OUT</div>
</div>
```

---

### CSS - Grid Layout

**Before** (main.html, line 425):
```css
.parts-list-header {
    grid-template-columns: 1.5fr 2.5fr 150px 200px 200px;
    gap: 1.5rem;
}

.parts-list-item {
    grid-template-columns: 1.5fr 2.5fr 150px 200px 200px;
    gap: 1.5rem;
}
```

**After** (main.html, line 425-445):
```css
.parts-list-header {
    grid-template-columns: 1.2fr 2fr 0.8fr 1fr 1fr 1fr 1.2fr 1fr 0.8fr;
    gap: 1rem;
    font-size: 0.75rem;  /* Adjusted for more columns */
}

.parts-list-item {
    grid-template-columns: 1.2fr 2fr 0.8fr 1fr 1fr 1fr 1.2fr 1fr 0.8fr;
    gap: 1rem;
}
```

---

### CSS - New Classes

**Added** (main.html, line 545-595):
```css
.item-stock {
    font-weight: 600;
    color: #10b981;
    font-size: 1rem;
}

.item-price {
    color: #0891b2;
    font-weight: 600;
    font-size: 0.95rem;
}

.item-description {
    color: #6b7280;
    font-size: 0.875rem;
    max-width: 150px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.replacement-code {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'Courier New', monospace;
}

.build-out-badge {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    padding: 0.35rem 0.65rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
}
```

---

### JavaScript - Data Population

**Before** (main.html, lines 960-992):
```javascript
parts.forEach(part => {
    // ... stok & machines logic ...
    
    item.innerHTML = `
        <div class="item-code">${part.part_code}</div>
        <div class="item-name">${part.part_name}</div>
        <div class="item-actions">
            <span class="stock-badge ${stockClass}">${part.stock}</span>
        </div>
        <div class="item-supplier">${part.supplier || '-'}</div>
        <div class="item-machines">${machinesHtml}</div>
    `;
});
```

**After** (main.html, lines 960-992):
```javascript
parts.forEach(part => {
    // Stock status logic
    let stockClass = part.stock <= part.critical_stock ? 'stock-critical' : 
                     part.stock <= part.critical_stock * 1.5 ? 'stock-low' : 'stock-ok';

    // Replacement code badge
    let replacementHtml = '-';
    if (part.replacement_code) {
        replacementHtml = `<span class="replacement-code">${part.replacement_code}</span>`;
    }

    // Build out badge
    let buildOutHtml = '<span style="color: #9ca3af;">-</span>';
    if (part.build_out) {
        buildOutHtml = '<span class="build-out-badge">🔴 BUILD OUT</span>';
    }

    item.innerHTML = `
        <div class="item-code">${part.part_code}</div>
        <div class="item-name">${part.part_name}</div>
        <div class="item-stock">${part.stock || 0}</div>
        <div class="item-supplier">${part.supplier || '-'}</div>
        <div class="item-price">${part.purchase_price_eur ? part.purchase_price_eur.toFixed(2) + ' €' : '-'}</div>
        <div class="item-description">${part.description ? part.description.substring(0, 20) + (part.description.length > 20 ? '...' : '') : '-'}</div>
        <div class="item-price">${part.sale_price_eur ? part.sale_price_eur.toFixed(2) + ' €' : '-'}</div>
        <div class="item-replacement">${replacementHtml}</div>
        <div>${buildOutHtml}</div>
    `;
});
```

---

## Warning System

### Detail Page - displayPartInfo Function

**Added** (detail.html, line 396-425):
```javascript
function displayPartInfo(part) {
    // ... existing code ...
    
    // ← NEW: Uyarı banner HTML
    let warningBanner = '';
    if (part.replacement_code) {
        warningBanner += `
            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                        border-left: 4px solid #f59e0b; padding: 1rem 1.5rem; 
                        border-radius: 8px; margin-bottom: 1.5rem; display: flex; 
                        align-items: center; gap: 1rem;">
                <i class="bi bi-exclamation-triangle" style="font-size: 1.5rem; color: #d97706;"></i>
                <div>
                    <strong style="color: #92400e;">⚠️ Bu parçanın değişen kodu var!</strong>
                    <p style="color: #b45309; margin: 0.25rem 0 0 0; font-size: 0.9rem;">
                        Yeni parça kodu: <strong>${part.replacement_code}</strong>
                    </p>
                </div>
            </div>
        `;
    }
    if (part.build_out) {
        warningBanner += `
            <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                        border-left: 4px solid #ef4444; padding: 1rem 1.5rem; 
                        border-radius: 8px; margin-bottom: 1.5rem; display: flex; 
                        align-items: center; gap: 1rem;">
                <i class="bi bi-exclamation-circle" style="font-size: 1.5rem; color: #dc2626;"></i>
                <div>
                    <strong style="color: #991b1b;">🔴 BUILD OUT - SİPARİŞ ETMEYİN!</strong>
                    <p style="color: #b91c1c; margin: 0.25rem 0 0 0; font-size: 0.9rem;">
                        Bu parça artık satın alınamaz veya kullanılamaz.
                    </p>
                </div>
            </div>
        `;
    }

    let infoHtml = warningBanner + `
        <!-- Rest of HTML follows -->
    `;
    
    // ... rest of existing code ...
}
```

---

## Summary of Changes

| Component | Lines | Changes | Status |
|-----------|-------|---------|--------|
| app.py | 3474-3542 | Updated API `/get_all` | ✅ |
| main.html | 425-445 | Grid layout 5→9 columns | ✅ |
| main.html | 545-595 | Added 6 new CSS classes | ✅ |
| main.html | 626-637 | Updated 5→9 table headers | ✅ |
| main.html | 960-992 | Updated JavaScript displayParts() | ✅ |
| detail.html | 396-425 | Added warning alerts | ✅ |

**Total Changes**: 6 sections across 3 files

---

## Testing Commands

```bash
# Verify database columns exist
mysql> DESCRIBE parts_info;
# Should show: replacement_code, build_out

# Test API endpoint
curl -X GET "http://localhost:5002/api/parts_info/get_all" \
  -H "Authorization: Bearer <token>"
# Should include: replacement_code, build_out in JSON

# Check for errors
# 1. Open browser console: F12
# 2. Go to http://192.168.10.27:5002/parts_info/
# 3. No errors should appear in console
```

---

## Rollback Instructions (If Needed)

To rollback these changes:

1. **Remove database columns** (optional, data-safe):
   ```sql
   ALTER TABLE parts_info DROP COLUMN replacement_code;
   ALTER TABLE parts_info DROP COLUMN build_out;
   ```

2. **Revert app.py** changes (lines 3474-3542)

3. **Revert main.html** to previous grid-template-columns

4. **Revert detail.html** by removing warning banner code

5. **Restart application**

**Note**: Database columns can stay - they just won't be used if code is reverted.

---

