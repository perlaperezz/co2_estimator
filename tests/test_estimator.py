from src.services.parser import parse_text


SAMPLE_INVOICE = """Invoice #INV-2024-0789
Supplier: EcoSupply Global Ltd
Date: 2024-11-15

Item                        Qty    Unit       Unit Price   Total
Freight shipping - ocean     2    container  $2,500.00    $5,000.00
Steel beams                  10   tonnes     $1,200.00    $12,000.00
Business class flights NYC   4    ticket     $1,800.00    $7,200.00
Hotel accommodation          6    nights     $350.00      $2,100.00
Consulting fees              40   hours      $250.00      $10,000.00
Packaging materials          500  boxes      $12.00       $6,000.00
Software license             12   months     $800.00      $9,600.00

                                              Total: $51,900.00
"""


def test_parse_sample():
    items, total = parse_text(SAMPLE_INVOICE)
    assert len(items) > 0, "Should parse at least one line item"
    assert total > 0, "Total should be positive"
    print(f"Parsed {len(items)} items, total=${total:.2f}")
    for item in items:
        print(f"  {item.description}: qty={item.quantity}, total=${item.total_price}")


if __name__ == "__main__":
    test_parse_sample()
