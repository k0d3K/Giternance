import { Slot } from "./calendar";

function isValidRepoLink(link: string): boolean {
	link = link.trim();
	if (link.length === 0)
		return false;
	if (link.startsWith('git@')) {
		const parts = link.split(':');
		if (parts.length !== 2)
			return false;

		const repoParts = parts[1].split('/');
		return repoParts.length >= 2;
	}
	try {
		const url = new URL(link);
		const repoParts = url.pathname.replace(/^\/+/, '').split('/');

		return repoParts.length >= 2;
	} catch {
		return false;
	}
}

function isValidCalendar(calendar: Slot[]): boolean {
	return calendar.length > 0;
}

export { isValidRepoLink, isValidCalendar };
