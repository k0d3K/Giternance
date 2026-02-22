import { Slot } from "./calendar";
import { inform, RepoLinks } from "./intercat";

enum METHODS {
	GET = 'GET',
	POST = 'POST'
};

function createRequestContent(method: METHODS, content=''): RequestInit {
	return {
		method: method,
		headers: { "Content-Type": "application/json" },
		body: content,
	};
}

async function sendRequestToBack<T>(method: METHODS, endpoint: string, content=''): Promise<T | boolean> {
	const res: Response = await fetch(endpoint, createRequestContent(method, content));
	if (!res.ok) {
		inform(res.statusText);
		return false;
	}
	try {
		const text = await res.text();
		if (!text || text === 'null')
			return true;
		const reply: T = JSON.parse(text);
		return reply;
	} catch {
		inform('Internal backup error');
		return false;
	}
}

/**
 * MODIFY DATA
 */

async function sendRepoLinks(repos: RepoLinks): Promise<boolean> {
	return await sendRequestToBack(METHODS.POST, '/api/repos', JSON.stringify(repos)) === true;
}

async function sendCalendar(calendar: Slot[]): Promise<boolean> {
	return await sendRequestToBack(METHODS.POST, '/api/calendar', JSON.stringify(calendar)) === true;
}

async function enableSync(): Promise<boolean> {
	return await sendRequestToBack(METHODS.POST, '/api/sync', 'true') === true;
}

async function disableSync(): Promise<boolean> {
	return await sendRequestToBack(METHODS.POST, '/api/sync', 'false') === true;
}

/**
 * CONSULT DATA
 */

async function askRepoLinks(): Promise<RepoLinks> {
	const reply = await sendRequestToBack<RepoLinks>(METHODS.GET, '/api/repos');
	if (typeof reply === 'boolean') {
		return {
			src: '',
			dst: ''
		};
	}
	return reply;
}

async function askCalendar(calendar: Slot[]): Promise<Slot[]> {
	const reply = await sendRequestToBack<Slot[]>(METHODS.GET, '/api/calendar');
	if (typeof reply === 'boolean') {
		return [];
	}
	return reply;
}

async function getSyncStatus(): Promise<boolean> {
	return await sendRequestToBack(METHODS.GET, '/api/status') === true;
}

export { sendRepoLinks, sendCalendar, enableSync, disableSync, askRepoLinks, askCalendar, getSyncStatus };
