# Day 7 – Food & Grocery Ordering Voice Agent

A voice-powered shopping assistant for food ordering and quick commerce platforms.

## Overview

Build a shopping assistant that helps users browse a catalog, add items to a cart, and place orders through natural voice conversations.

## Features Implemented

### ✅ Primary Goal (MVP)

1. **Product Catalog** (`catalog.json`)
   - 15 items across multiple categories (Groceries, Snacks)
   - Each item includes: id, name, category, price, unit, tags
   - Items: bread, eggs, milk, pasta, chicken, cheese, produce, snacks, etc.

2. **Cart Management**
   - `add_item(item_name, quantity)` - Add items with quantities
   - `remove_item(item_name)` - Remove items from cart
   - `update_quantity(item_name, quantity)` - Update item quantities
   - `list_cart()` - Show cart contents with total price

3. **Catalog Browsing**
   - `browse_catalog(category)` - Browse all items or filter by category
   - `search_catalog(search_term)` - Search by name, tags, or category

4. **Order Placement**
   - `place_order(customer_name, address)` - Save order to JSON file
   - Order confirmation with total and order ID
   - Cart automatically cleared after order placement
   - Orders saved to `orders/order_[Name]_[Timestamp].json`

### ✅ Advanced Features

5. **Recipe Intelligence**
   - `ingredients_for(dish, servings)` - Add recipe ingredients to cart
   - Pre-configured recipes: peanut butter sandwich, pasta for two, omelette
   - Automatically adds all required ingredients

6. **Order Tracking**
   - `check_order_status(order_id)` - Check current order status
   - `mock_progress_order(order_id, next_status)` - Update order status
   - Status progression: placed → preparing → out_for_delivery → delivered

## Project Structure

```
Day 7/
├── backend/
│   ├── src/
│   │   └── order_agent.py          # Main agent implementation
│   ├── catalog.json                 # Product catalog
│   ├── orders/                      # Order JSON files (generated)
│   ├── pyproject.toml              # Python dependencies
│   └── .env.local                  # API keys (not in repo)
├── frontend/
│   ├── app/                        # Next.js app
│   ├── components/                 # React components
│   ├── package.json                # Node dependencies
│   └── .env.local                  # LiveKit credentials (not in repo)
└── README.md                       # This file
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd "Day 7/backend"
   ```

2. **Install dependencies:**
   ```bash
   pip install livekit-agents livekit-plugins-deepgram livekit-plugins-google livekit-plugins-murf livekit-plugins-silero
   ```

3. **Create `.env.local` file:**
   ```env
   LIVEKIT_URL=wss://your-livekit-url
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   DEEPGRAM_API_KEY=your-deepgram-key
   GOOGLE_API_KEY=your-google-key
   MURF_API_KEY=your-murf-key
   ```

4. **Run the agent:**
   ```bash
   python src/order_agent.py dev
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd "Day 7/frontend"
   ```

2. **Install dependencies:**
   ```bash
   pnpm install
   ```

3. **Create `.env.local` file:**
   ```env
   LIVEKIT_URL=wss://your-livekit-url
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   ```

4. **Run the frontend:**
   ```bash
   pnpm dev
   ```

5. **Open browser:**
   Navigate to http://localhost:3000

## Usage Examples

### Browse Catalog
- "What's in the catalog?"
- "Show me all groceries"
- "Do you have any dairy products?"
- "Search for bread"

### Add Items to Cart
- "Add 2 eggs to my cart"
- "I need 1 loaf of bread"
- "Add 3 bottles of milk"

### Recipe-Based Shopping
- "I need ingredients for pasta for two"
- "Add ingredients for a peanut butter sandwich"
- "Get me what I need for an omelette"

### View Cart
- "What's in my cart?"
- "Show me my cart"
- "List my items"

### Place Order
- "Place my order for John Doe at 123 Main St"
- "I'm ready to checkout"
- "Complete my order"

### Track Order
- "What's the status of my order?"
- "Check order order_John_Doe_20251127234036.json"

## Technical Stack

- **Framework:** LiveKit Agents (Python)
- **STT:** Deepgram Nova-3
- **LLM:** Google Gemini 2.5 Flash
- **TTS:** Murf Falcon (en-US-matthew voice)
- **VAD:** Silero
- **Frontend:** Next.js with React
- **Package Manager:** pnpm

## Order Data Structure

Orders are saved as JSON files in `backend/orders/`:

```json
{
  "customer_name": "John Doe",
  "address": "123 Main St",
  "items": [
    {
      "id": "eggs_large",
      "name": "Large Eggs (12 pack)",
      "quantity": 2,
      "unit_price": 3.99,
      "line_total": 7.98
    }
  ],
  "total": 7.98,
  "timestamp": "2025-11-27T23:40:36.556736",
  "status": "placed",
  "status_history": [
    {
      "status": "placed",
      "timestamp": "2025-11-27T23:40:36.556746"
    }
  ]
}
```

## Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [Function Tools](https://docs.livekit.io/agents/build/tools/)
- [Prompting Guide](https://docs.livekit.io/agents/build/prompting/)

## License

MIT

