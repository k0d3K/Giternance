import { disableSync, enableSync, sendCalendar, sendRepoLinks } from "./api";
import { getCalendar } from "./calendar";
import { isValidCalendar, isValidRepoLink } from "./dataValidation";
import { getRepolinks, inform } from "./intercat";

function setupButtonSync(): void {
	const btn = document.getElementById('sync');
	if (!(btn instanceof HTMLButtonElement))
		return;
	btn.addEventListener('click', askForSync);
}

async function askForSync(): Promise<void> {
	const repos = getRepolinks();
	if (!isValidRepoLink(repos.src)) {
		inform("Invalid source repository");
		return;
	}
	if (!isValidRepoLink(repos.dst)) {
		inform("Invalid target repository");
		return;
	}
	const calendar = getCalendar();
	if (!isValidCalendar(calendar)) {
		inform("Please select at least one slot");
		return;
	}
	if (!await sendRepoLinks(repos))
		return;
	if (!await sendCalendar(calendar))
		return;
	if (!await enableSync())
		return;
	const btn = document.getElementById('sync');
	if (!(btn instanceof HTMLButtonElement))
		return;
	btn.value = 'Stop sync';
	btn.removeEventListener('click', askForSync);
	btn.addEventListener('click', stopSync);
}

async function stopSync(): Promise<void> {
	if (!await disableSync())
		return;
	const btn = document.getElementById('sync');
	if (!(btn instanceof HTMLButtonElement))
		return;
	btn.value = 'Synchronize';
	btn.removeEventListener('click', stopSync);
	btn.addEventListener('click', askForSync);
}

export { setupButtonSync };
