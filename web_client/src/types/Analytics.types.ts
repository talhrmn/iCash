export interface UniqueBuyersResponse {
	unique_buyers_count: number;
}

export interface LoyalCustomer {
	user_id: string;
	purchase_count: number;
}

export interface LoyalCustomersResponse {
	loyal_customers: LoyalCustomer[];
	criteria: string;
	total_loyal_customers: number;
}

export interface TopSellingProduct {
	product_name: string;
	total_sold: number;
	rank: number;
}

export interface TopSellingProductsResponse {
	top_selling_products: TopSellingProduct[];
}

export interface AnalyticsData {
	uniqueBuyers: UniqueBuyersResponse;
	loyalCustomers: LoyalCustomersResponse;
	topSellingProducts: TopSellingProductsResponse;
}
