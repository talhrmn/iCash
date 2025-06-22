export const API_CONFIG = {
	CASH_REGISTER_BASE_URL: import.meta.env.VITE_API_CASH_REGISTER_BASE_URL,
	ANALYTICS_BASE_URL: import.meta.env.VITE_ANALYTICS_API_BASE_URL,
	CASH_REGISTER: {
		PREFIX: "/api/cash-register",
	},
	ANALYTICS: {
		PREFIX: "/api/analytics",
	},
} as const;

export const QUERY_KEYS = {
	BRANCHES: ["branches"] as const,
	PRODUCTS: ["products"] as const,
	ANALYTICS: ["analytics"] as const,
	UNIQUE_BUYERS: ["analytics", "unique-buyers"] as const,
	LOYAL_CUSTOMERS: ["analytics", "loyal-customers"] as const,
	TOP_PRODUCTS: ["analytics", "top-products"] as const,
} as const;

export const getApiUrl = (
	service: "CASH_REGISTER" | "ANALYTICS",
	endpoint: string
) => {
	const baseUrl =
		service === "ANALYTICS"
			? API_CONFIG.ANALYTICS_BASE_URL
			: API_CONFIG.CASH_REGISTER_BASE_URL;
	const prefix = API_CONFIG[service].PREFIX;
	return `${baseUrl}${prefix}${endpoint}`;
};

export const handleApiError = (error: Error) => {
	console.error("API Error:", error);
	throw new Error(error.message || "An error occurred");
};
