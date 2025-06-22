export interface Branch {
	id: string;
}

export interface Product {
	id: string;
	product_name: string;
	unit_price: number;
}

export interface ProductItem {
	product_name: string;
	quantity: number;
}

export interface PurchaseRequest {
	supermarket_id: string;
	user_id?: string;
	items: ProductItem[];
}
