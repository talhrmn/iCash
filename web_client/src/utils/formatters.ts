export const toTitleCase = (str: string) => {
	return str.replace(/\w+/g, (word) => {
		return word.charAt(0).toUpperCase() + word.substring(1).toLowerCase();
	});
};
