const MAX_LOGS = 25;

function addMessageInDiv(div: HTMLElement, message: string): void {
	const logEntry = document.createElement('p');
	logEntry.textContent = message;
	div.appendChild(logEntry);
	div.scrollTop = div.scrollHeight;
}

function setupLogs(): void {
	const socket = new WebSocket(`/ws/logs`);

	socket.onmessage = (event: MessageEvent): void => {
		const message = event.data;

		const logs = document.getElementById('logs');
		if (!(logs instanceof HTMLElement))
			return;
		addMessageInDiv(logs, message);

		while (logs.children.length > MAX_LOGS) {
			const first = logs.firstElementChild;
			if (!first)
				break;
			logs.removeChild(first);
		}
	};

	socket.onerror = (): void => {
		console.error("WebSocket error");
	};
}

export { setupLogs };
