import json
from pathlib import Path
from datetime import datetime

ORDERS_DIR = Path('orders')

PROGRESSION = ['placed','preparing','out_for_delivery','delivered']


def progress_order(path: Path):
    with open(path, 'r') as f:
        order = json.load(f)
    current = order.get('status','placed')
    try:
        idx = PROGRESSION.index(current)
        new_status = PROGRESSION[min(idx+1, len(PROGRESSION)-1)]
    except ValueError:
        new_status = 'placed'
    order['status'] = new_status
    order.setdefault('status_history',[]).append({'status': new_status, 'timestamp': datetime.now().isoformat()})
    with open(path, 'w') as f:
        json.dump(order, f, indent=2)
    return path.name, new_status


if __name__ == '__main__':
    if not ORDERS_DIR.exists():
        print('No orders dir')
        raise SystemExit(1)
    for p in sorted(ORDERS_DIR.glob('order_*.json')):
        name, ns = progress_order(p)
        print(f'Updated {name} -> {ns}')
