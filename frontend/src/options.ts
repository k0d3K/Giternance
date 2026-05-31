import { askRepoLinks, disableSync, enableSync, sendCalendar, sendRepoLinks } from "./api";
import { getCalendar } from "./calendar";
import { isValidCalendar, isValidRepoLink } from "./dataValidation";
import { getRepolinks, inform } from "./intercat";

function setupOptions(): void {
	setupReposLinks();
	setupButtonSync();
}

async function setupReposLinks(): Promise<void> {
	const src = document.getElementById('sourceRepo');
	const dst = document.getElementById('targetRepo');
	if (!(src instanceof HTMLInputElement) || !(dst instanceof HTMLInputElement))
		return;
	const links = await askRepoLinks();
	if (links.src)
		src.value = links.src;
	if (links.dst)
		dst.value = links.dst;
}

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
	const btnTxt = document.getElementById('syncText');
	if (!(btn instanceof HTMLButtonElement) || !btnTxt)
		return;
	btnTxt.innerHTML = 'Stop sync';
	btn.removeEventListener('click', askForSync);
	btn.addEventListener('click', stopSync);
}

async function stopSync(): Promise<void> {
	if (!await disableSync())
		return;
	const btn = document.getElementById('sync');
	const btnTxt = document.getElementById('syncText');
	if (!(btn instanceof HTMLButtonElement) || !btnTxt)
		return;
	btnTxt.innerHTML = 'Synchronize';
	btn.removeEventListener('click', stopSync);
	btn.addEventListener('click', askForSync);
}

export { setupOptions };
