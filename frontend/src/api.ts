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

async function sendRequestToBack(method: METHODS, endpoint: string, content=''): Promise<Response> {
	return await fetch(endpoint, createRequestContent(method, content));
}

async function sendRepoLinks(repos: RepoLinks): Promise<boolean> {
	const res: Response = await sendRequestToBack(METHODS.POST, '/api/repos', JSON.stringify(repos));
	if (!res.ok) {
		inform(res.statusText);
		return false;
	}
	return true;
}

async function sendCalendar(calendar: Slot[]): Promise<boolean> {
	const res: Response = await sendRequestToBack(METHODS.POST, '/api/calendar', JSON.stringify(calendar));
	if (!res.ok) {
		inform(res.statusText);
		return false;
	}
	return true;
}

async function enableSync(): Promise<boolean> {
	const res: Response = await sendRequestToBack(METHODS.POST, '/api/enable');
	if (!res.ok) {
		inform(res.statusText);
		return false;
	}
	return true;
}

async function disableSync(): Promise<boolean> {
	const res: Response = await sendRequestToBack(METHODS.POST, '/api/disable');
	if (!res.ok) {
		inform(res.statusText);
		return false;
	}
	return true;
}

export { sendRepoLinks, sendCalendar, enableSync, disableSync };
