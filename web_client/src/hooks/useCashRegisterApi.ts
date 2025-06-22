import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { QUERY_KEYS } from "../config/api.config";

import type {
	Branch,
	Product,
	PurchaseRequest,
} from "../types/CashRegister.types";
import { cashRegisterApiClient } from "../services/CashRegisterApi.client";

export const useBranches = () => {
	return useQuery({
		queryKey: QUERY_KEYS.BRANCHES,
		queryFn: async (): Promise<Branch[]> => {
			const response = await cashRegisterApiClient.getBranches();
			return response.data;
		},
		staleTime: 5 * 60 * 1000,
		retry: 3,
	});
};

export const useProducts = () => {
	return useQuery({
		queryKey: QUERY_KEYS.PRODUCTS,
		queryFn: async (): Promise<Product[]> => {
			const response = await cashRegisterApiClient.getProducts();
			return response.data;
		},
		staleTime: 5 * 60 * 1000,
		retry: 3,
	});
};

export const useCreatePurchase = () => {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: async (purchaseData: PurchaseRequest) => {
			const response = await cashRegisterApiClient.createPurchase(purchaseData);
			return response.data;
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: QUERY_KEYS.ANALYTICS });
		},
		onError: (error) => {
			console.error("Purchase creation failed:", error);
		},
	});
};
