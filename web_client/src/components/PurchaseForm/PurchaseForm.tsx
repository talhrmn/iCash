import React, {
	useCallback,
	useEffect,
	useMemo,
	useRef,
	useState,
} from "react";
import {
	useBranches,
	useCreatePurchase,
	useProducts,
} from "../../hooks/useCashRegisterApi";
import type { PurchaseRequest } from "../../types/CashRegister.types";
import { toTitleCase } from "../../utils/formatters";
import { ErrorMessage } from "../ui/ErrorMessage/ErrorMessage";
import { LoadingSpinner } from "../ui/LoadingSpinner/LoadingSpinner";
import styles from "./PurchaseForm.module.css";

interface SelectedProduct {
	id: string;
	product_name: string;
	unit_price: number;
}

export const PurchaseForm: React.FC = () => {
	const {
		data: branches = [],
		isLoading: isLoadingBranches,
		error: branchesError,
	} = useBranches();

	const {
		data: products = [],
		isLoading: isLoadingProducts,
		error: productsError,
	} = useProducts();

	const createPurchase = useCreatePurchase();

	const [formData, setFormData] = useState({
		branchId: "",
		userId: "",
	});

	const [selectedProducts, setSelectedProducts] = useState<SelectedProduct[]>(
		[]
	);
	const [isDropdownOpen, setIsDropdownOpen] = useState(false);
	const [successMessage, setSuccessMessage] = useState("");
	const dropdownRef = useRef<HTMLDivElement>(null);

	const allProducts = useMemo(() => {
		return products.map((product) => ({
			...product,
			product_name: toTitleCase(product.product_name),
		}));
	}, [products]);

	const totalSum = useMemo(() => {
		return selectedProducts.reduce(
			(sum, product) => sum + product.unit_price,
			0
		);
	}, [selectedProducts]);

	useEffect(() => {
		const handleClickOutside = (event: MouseEvent) => {
			if (
				dropdownRef.current &&
				!dropdownRef.current.contains(event.target as Node)
			) {
				setIsDropdownOpen(false);
			}
		};

		document.addEventListener("mousedown", handleClickOutside);
		return () => {
			document.removeEventListener("mousedown", handleClickOutside);
		};
	}, []);

	const handleBranchChange = useCallback(
		(branchId: string) => {
			setFormData((prev) => ({ ...prev, branchId }));
			if (successMessage) setSuccessMessage("");
		},
		[successMessage]
	);

	const handleInputChange = useCallback(
		(field: string, value: string) => {
			setFormData((prev) => ({ ...prev, [field]: value }));
			if (successMessage) setSuccessMessage("");
		},
		[successMessage]
	);

	const handleProductToggle = useCallback(
		(productId: string) => {
			const product = allProducts.find((p) => p.id === productId);
			if (!product) return;

			setSelectedProducts((prev) => {
				const existingIndex = prev.findIndex((p) => p.id === product.id);
				if (existingIndex === -1) {
					return [
						...prev,
						{
							id: product.id,
							product_name: product.product_name,
							unit_price: product.unit_price,
						},
					];
				} else {
					return prev.filter((_, index) => index !== existingIndex);
				}
			});

			if (successMessage) setSuccessMessage("");
		},
		[allProducts, successMessage]
	);

	const isProductSelected = useCallback(
		(productId: string) => {
			return selectedProducts.some((p) => p.id === productId);
		},
		[selectedProducts]
	);

	const handleSubmit = useCallback(
		async (e: React.FormEvent) => {
			e.preventDefault();

			if (!formData.branchId || selectedProducts.length === 0) return;

			try {
				const purchaseData: PurchaseRequest = {
					supermarket_id: formData.branchId,
					items: selectedProducts.map((product) => ({
						product_name: product.product_name.toLowerCase(),
						quantity: 1,
					})),
				};

				if (formData.userId) purchaseData.user_id = formData.userId;

				await createPurchase.mutateAsync(purchaseData);

				setSuccessMessage(
					`${selectedProducts.length} purchases created successfully!`
				);
				setFormData({ branchId: "", userId: "" });
				setSelectedProducts([]);
			} catch (error) {
				console.error("Purchase failed:", error);
			}
		},
		[formData.branchId, formData.userId, selectedProducts, createPurchase]
	);

	const isLoading = isLoadingBranches || isLoadingProducts;
	const hasError = branchesError || productsError;
	const isFormValid = formData.branchId && selectedProducts.length > 0;

	if (isLoading) {
		return <LoadingSpinner message="Loading form data..." />;
	}

	if (hasError) {
		return <ErrorMessage message="Failed to load form data" />;
	}

	return (
		<div className={styles.container}>
			<header className={styles.header}>
				<h1>New Purchase</h1>
			</header>

			<form onSubmit={handleSubmit} className={styles.form}>
				<div className={styles.formGroup}>
					<label htmlFor="branch" className={styles.label}>
						Branch *
					</label>
					<select
						id="branch"
						value={formData.branchId}
						onChange={(e) => handleBranchChange(e.target.value)}
						className={styles.select}
						required
					>
						<option value="">Select a branch</option>
						{branches.map((branch) => (
							<option key={branch.id} value={branch.id}>
								{branch.id}
							</option>
						))}
					</select>
				</div>

				<div className={styles.formGroup}>
					<label htmlFor="userId" className={styles.label}>
						User ID *
					</label>
					<input
						type="text"
						id="userId"
						value={formData.userId}
						placeholder="Leave empty if not registered"
						onChange={(e) => handleInputChange("userId", e.target.value)}
						className={styles.input}
					/>
				</div>

				<div className={styles.formGroup} ref={dropdownRef}>
					<label className={styles.label}>
						Products ({selectedProducts.length} selected)
					</label>
					<div className={styles.customDropdown}>
						<button
							type="button"
							className={styles.dropdownToggle}
							onClick={() => setIsDropdownOpen(!isDropdownOpen)}
							aria-expanded={isDropdownOpen}
						>
							{selectedProducts.length > 0
								? selectedProducts.map((p) => p.product_name).join(", ")
								: "Select products..."}
							<span
								className={`${styles.dropdownArrow} ${
									isDropdownOpen ? styles.open : ""
								}`}
							>
								▼
							</span>
						</button>

						{isDropdownOpen && (
							<div className={styles.dropdownMenu}>
								{allProducts.map((product) => (
									<label key={product.id} className={styles.checkboxItem}>
										<input
											type="checkbox"
											checked={isProductSelected(product.id)}
											onChange={() => handleProductToggle(product.id)}
											className={styles.checkbox}
										/>
										<span className={styles.checkboxLabel}>
											{product.product_name} - ${product.unit_price.toFixed(2)}
										</span>
									</label>
								))}
							</div>
						)}
					</div>
				</div>

				<div className={styles.totalSection}>
					<span className={styles.totalLabel}>Total:</span>
					<span className={styles.totalAmount}>${totalSum.toFixed(2)}</span>
				</div>

				{successMessage && (
					<div className={styles.successMessage}>{successMessage}</div>
				)}

				{createPurchase.error && (
					<div className={styles.errorMessage}>
						Failed to create purchase. Please try again.
					</div>
				)}

				<button
					type="submit"
					className={styles.submitButton}
					disabled={!isFormValid || createPurchase.isPending}
				>
					{createPurchase.isPending ? "Creating..." : "Create Purchase"}
				</button>
			</form>
		</div>
	);
};
