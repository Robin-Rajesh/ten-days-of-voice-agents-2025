import asyncio
import json
from pathlib import Path
from datetime import datetime

from src.order_agent import OrderAgent, load_catalog


async def run_simulation():
    agent = OrderAgent()

    print(await agent.greet(None))

    # Add explicit item
    print("[User] Add 2 Whole Wheat Bread")
    print(await agent.add_item(None, "Whole Wheat Bread", 2))

    # Add items by 'ingredients for' mapping
    print("[User] I need ingredients for peanut butter sandwich")
    print(await agent.ingredients_for(None, "peanut butter sandwich", 1))

    # List cart
    print(await agent.list_cart(None))

    # Place order
    place_result = await agent.place_order(None, customer_name="John Doe", address="123 Demo St")
    print(place_result)
    # Extract order id from place_result (filename at end)
    if 'Your order id is' in place_result:
        order_id = place_result.split('Your order id is')[-1].strip().rstrip('.')
    else:
        # find last order file
        orders_dir = Path('orders')
        files = sorted(orders_dir.glob('order_*.json'))
        order_id = files[-1].name if files else None
    if order_id:
        # check status
        print(await agent.check_order_status(None, order_id))
        # progress status
        print(await agent.mock_progress_order(None, order_id))
        print(await agent.check_order_status(None, order_id))
        print(await agent.mock_progress_order(None, order_id))
        print(await agent.check_order_status(None, order_id))
    else:
        print('Could not determine order id')


if __name__ == '__main__':
    asyncio.run(run_simulation())
