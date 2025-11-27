from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import json
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CATALOG_PATH = Path("catalog.json")
ORDERS_DIR = Path("orders")
ORDERS_DIR.mkdir(exist_ok=True)
CART_PATH = Path("cart.json")

class AddItem(BaseModel):
    item_id: str
    quantity: int = 1

class IngredientsRequest(BaseModel):
    dish: str
    servings: int = 1

class PlaceOrderRequest(BaseModel):
    customer_name: str | None = None
    address: str | None = None


def load_catalog():
    if not CATALOG_PATH.exists():
        return []
    return json.loads(CATALOG_PATH.read_text())


def load_cart():
    if not CART_PATH.exists():
        return {}
    return json.loads(CART_PATH.read_text())


def save_cart(cart):
    CART_PATH.write_text(json.dumps(cart, indent=2))


@app.get('/api/catalog')
async def get_catalog():
    return load_catalog()


@app.get('/api/cart')
async def get_cart():
    return load_cart()


@app.post('/api/cart/add')
async def add_to_cart(req: AddItem):
    catalog = load_catalog()
    item = next((i for i in catalog if i['id'] == req.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    cart = load_cart()
    entry = cart.get(req.item_id, {'item': item, 'quantity': 0})
    entry['quantity'] += req.quantity
    cart[req.item_id] = entry
    save_cart(cart)
    return {'status': 'ok', 'cart': cart}


RECIPES = {
    'peanut butter sandwich': ['bread_whole_wheat','peanut_butter'],
    'pasta for two': ['pasta_spaghetti','pasta_sauce','olive_oil'],
    'omelette': ['eggs_large','cheddar_cheese','milk_2l']
}


@app.post('/api/cart/ingredients')
async def ingredients(req: IngredientsRequest):
    dish = req.dish.lower()
    if dish not in RECIPES:
        raise HTTPException(status_code=404, detail='Recipe not found')
    catalog = load_catalog()
    cart = load_cart()
    added = []
    for iid in RECIPES[dish]:
        item = next((i for i in catalog if i['id'] == iid), None)
        if item:
            entry = cart.get(iid, {'item': item, 'quantity': 0})
            entry['quantity'] += req.servings
            cart[iid] = entry
            added.append(item['name'])
    save_cart(cart)
    return {'status': 'ok', 'added': added, 'cart': cart}


@app.post('/api/cart/remove')
async def remove_from_cart(req: AddItem):
    cart = load_cart()
    if req.item_id in cart:
        del cart[req.item_id]
        save_cart(cart)
        return {'status': 'ok', 'cart': cart}
    raise HTTPException(status_code=404, detail='Item not in cart')


@app.post('/api/cart/place')
async def place_order(req: PlaceOrderRequest):
    cart = load_cart()
    if not cart:
        raise HTTPException(status_code=400, detail='Cart empty')
    items = []
    total = 0.0
    for k, v in cart.items():
        qty = v['quantity']
        price = v['item']['price']
        items.append({'id': k, 'name': v['item']['name'], 'quantity': qty, 'unit_price': price, 'line_total': round(qty * price, 2)})
        total += qty * price
    order = {
        'customer_name': req.customer_name or 'Guest',
        'address': req.address or '',
        'items': items,
        'total': round(total, 2),
        'timestamp': datetime.now().isoformat(),
        'status': 'placed',
        'status_history': [{'status': 'placed', 'timestamp': datetime.now().isoformat()}]
    }
    fname = f"order_{order['customer_name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    path = ORDERS_DIR / fname
    path.write_text(json.dumps(order, indent=2))
    # clear cart
    save_cart({})
    return {'status': 'ok', 'order_id': fname}


@app.get('/api/orders')
async def list_orders():
    files = sorted(ORDERS_DIR.glob('order_*.json'))
    return [f.name for f in files]


@app.get('/api/order/{order_id}')
async def get_order(order_id: str):
    path = ORDERS_DIR / order_id
    if not path.exists():
        matches = list(ORDERS_DIR.glob(f"{order_id}*.json"))
        if not matches:
            raise HTTPException(status_code=404, detail='Order not found')
        path = matches[0]
    return json.loads(path.read_text())


@app.post('/api/order/{order_id}/progress')
async def progress_order(order_id: str):
    path = ORDERS_DIR / order_id
    if not path.exists():
        matches = list(ORDERS_DIR.glob(f"{order_id}*.json"))
        if not matches:
            raise HTTPException(status_code=404, detail='Order not found')
        path = matches[0]
    order = json.loads(path.read_text())
    prog = ['placed','preparing','out_for_delivery','delivered']
    current = order.get('status','placed')
    try:
        idx = prog.index(current)
        new = prog[min(idx+1, len(prog)-1)]
    except ValueError:
        new = 'placed'
    order['status'] = new
    order.setdefault('status_history', []).append({'status': new, 'timestamp': datetime.now().isoformat()})
    path.write_text(json.dumps(order, indent=2))
    return {'status': 'ok', 'new_status': new}
