import logging
import os
import sys
import uuid

import pandas as pd

from shared.database import SessionLocal
from shared.database.models import Product, Branch, User, Purchase, PurchaseItem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def load_products_bulk(session, csv_path: str) -> None:
    """
    Load products from CSV file into the database using bulk operations.
    """
    logger.info(f"Attempting to load products from: {csv_path}")

    if not os.path.isfile(csv_path):
        logger.error(f"Products CSV not found at {csv_path}")
        return

    try:
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded CSV with {len(df)} rows and columns: {list(df.columns)}")

        if not {"product_name", "unit_price"}.issubset(df.columns):
            logger.error("Products CSV missing required columns")
            return

        # Clean and validate data
        df = df.dropna(subset=["product_name", "unit_price"])
        df["product_name"] = df["product_name"].astype(str).str.strip()
        df = df[df["product_name"] != ""]

        # Convert price and filter valid ones
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
        df = df.dropna(subset=["unit_price"])
        df = df[df["unit_price"] >= 0]

        # Remove duplicates
        df = df.drop_duplicates(subset=["product_name"])

        logger.info(f"After cleaning: {len(df)} valid products")

        # Get existing products to avoid duplicates
        existing_products = set(
            session.query(Product.product_name).all()
        )
        existing_product_names = {name[0] for name in existing_products}

        # Filter out existing products
        new_products_df = df[~df["product_name"].isin(existing_product_names)]
        logger.info(f"Found {len(new_products_df)} new products to insert")

        if len(new_products_df) == 0:
            logger.info("No new products to insert")
            return

        # Prepare bulk insert data
        products_data = [
            {
                "product_name": row["product_name"],
                "unit_price": row["unit_price"]
            }
            for _, row in new_products_df.iterrows()
        ]

        # Bulk insert using SQLAlchemy bulk_insert_mappings
        session.bulk_insert_mappings(Product, products_data)
        session.commit()

        logger.info(f"Successfully bulk inserted {len(products_data)} products")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading products: {e}")
        raise


def load_purchases_bulk(session, csv_path: str) -> None:
    """
    Load purchases from CSV file into the database using bulk operations.
    """
    logger.info(f"Attempting to load purchases from: {csv_path}")

    if not os.path.isfile(csv_path):
        logger.error(f"Purchases CSV not found at {csv_path}")
        return

    df = pd.read_csv(csv_path, dtype=str)
    logger.info(f"Loaded purchases CSV with {len(df)} rows")

    required_columns = {"supermarket_id", "timestamp", "user_id", "items_list", "total_amount"}
    if not required_columns.issubset(df.columns):
        logger.error(f"Missing required columns: {required_columns - set(df.columns)}")
        return

    # Clean and validate data upfront
    df = df.dropna(subset=list(required_columns))
    df = df[df["supermarket_id"].str.strip() != ""]
    df = df[df["items_list"].str.strip() != ""]

    logger.info(f"After initial cleaning: {len(df)} valid purchase records")

    # Parse timestamps
    try:
        df["parsed_timestamp"] = pd.to_datetime(df["timestamp"])
    except Exception as e:
        logger.error(f"Error parsing timestamps: {e}")
        return

    # Validate UUIDs
    valid_uuids = []
    for idx, user_id_str in enumerate(df["user_id"]):
        try:
            uuid.UUID(user_id_str)
            valid_uuids.append(True)
        except:
            valid_uuids.append(False)
            logger.warning(f"Invalid UUID at row {idx}: {user_id_str}")

    df = df[valid_uuids]
    logger.info(f"After UUID validation: {len(df)} valid records")

    # Validate total_amount
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
    df = df.dropna(subset=["total_amount"])
    df = df[df["total_amount"] >= 0]

    logger.info(f"After amount validation: {len(df)} valid records")

    # Bulk create branches
    unique_branches = set(df["supermarket_id"].str.strip())
    existing_branches = set(
        branch[0] for branch in session.query(Branch.id).all()
    )
    new_branches = unique_branches - existing_branches

    if new_branches:
        branch_data = [{"id": branch_id} for branch_id in new_branches]
        session.bulk_insert_mappings(Branch, branch_data)
        logger.info(f"Bulk inserted {len(new_branches)} new branches")

    # Bulk create users
    unique_users = set(df["user_id"].str.strip())
    existing_users = set(
        str(user[0]) for user in session.query(User.id).all()
    )
    new_users = unique_users - existing_users

    if new_users:
        user_data = [{"id": uuid.UUID(user_id)} for user_id in new_users]
        session.bulk_insert_mappings(User, user_data)
        logger.info(f"Bulk inserted {len(new_users)} new users")

    # Get all products for mapping
    all_products = session.query(Product).all()
    product_name_to_id = {p.product_name: p.id for p in all_products}
    product_name_to_price = {p.product_name: p.unit_price for p in all_products}

    # Process purchases in batches
    BATCH_SIZE = 1000
    total_purchases = 0
    total_items = 0

    for batch_start in range(0, len(df), BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, len(df))
        batch_df = df.iloc[batch_start:batch_end]

        logger.info(f"Processing batch {batch_start + 1}-{batch_end} of {len(df)}")

        # Prepare purchase data
        purchase_data = []
        purchase_items_data = []

        for idx, row in batch_df.iterrows():
            try:
                # Parse items
                product_names = [p.strip() for p in row["items_list"].split(",") if p.strip()]

                # Check if all products exist
                missing_products = [name for name in product_names if name not in product_name_to_id]
                if missing_products:
                    logger.warning(f"Row {idx}: Missing products {missing_products}, skipping")
                    continue

                # Create purchase record
                purchase_id = str(uuid.uuid4())  # Generate UUID for purchase
                purchase_record = {
                    "id": purchase_id,
                    "supermarket_id": row["supermarket_id"].strip(),
                    "user_id": uuid.UUID(row["user_id"]),
                    "timestamp": row["parsed_timestamp"],
                    "total_amount": float(row["total_amount"])
                }
                purchase_data.append(purchase_record)

                # Create purchase items
                for product_name in product_names:
                    item_record = {
                        "id": str(uuid.uuid4()),  # Generate UUID for item
                        "purchase_id": purchase_id,
                        "product_id": product_name_to_id[product_name],
                        "quantity": 1,
                        "unit_price": product_name_to_price[product_name]
                    }
                    purchase_items_data.append(item_record)

            except Exception as e:
                logger.error(f"Error processing row {idx}: {e}")
                continue

        # Bulk insert batch
        if purchase_data:
            try:
                session.bulk_insert_mappings(Purchase, purchase_data)
                session.bulk_insert_mappings(PurchaseItem, purchase_items_data)
                session.commit()

                total_purchases += len(purchase_data)
                total_items += len(purchase_items_data)
                logger.info(f"Batch completed: {len(purchase_data)} purchases, {len(purchase_items_data)} items")

            except Exception as e:
                session.rollback()
                logger.error(f"Error inserting batch: {e}")
                continue

    logger.info(f"Purchases loading completed. Added {total_purchases} purchases with {total_items} items")


def main() -> None:
    """
    Main entry point for bulk data loading.
    """
    logger.info("Starting bulk data loading process")

    # Use the correct paths based on volume mounts
    products_path = '../data/products_list.csv'
    purchases_path = '../data/purchases.csv'

    logger.info(f"Using products path: {products_path}")
    logger.info(f"Using purchases path: {purchases_path}")

    # Check if files exist before proceeding
    if not os.path.exists('../data'):
        logger.error("/data directory not found - check volume mounts")
        return

    logger.info(f"Files in /data: {os.listdir('/data') if os.path.exists('/data') else 'directory not found'}")

    session = SessionLocal()
    try:
        load_products_bulk(session, products_path)
        load_purchases_bulk(session, purchases_path)
        logger.info("Bulk data loading completed successfully")
    except Exception as e:
        logger.error(f"Bulk data loading failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
