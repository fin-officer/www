# we have created four endpoints: `GET /items` to retrieve all items, `POST /items` to add a new item, `PUT /items/{item_id}` to update an existing item, and `DELETE /items/{item_id}` to delete an item. The API accepts and returns JSON data using the Pydantic model `Item`. The `data` list serves as a simple storage for the items, but you can replace it with a database or any other data source as per your requirements.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create FastAPI instance
app = FastAPI()

# Sample data storage
data = []

# Define request body model
class Item(BaseModel):
    name: str
    price: float

# GET request to retrieve all items
@app.get("/items")
def get_items():
    return data

# POST request to add a new item
@app.post("/items")
def add_item(item: Item):
    data.append(item)
    return {"message": "Item added successfully"}

# PUT request to update an existing item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id < len(data):
        data[item_id] = item
        return {"message": "Item updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE request to remove an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id < len(data):
        del data[item_id]
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
