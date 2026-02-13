interface RepoLinks {
	src: string,
	dst: string
}

function getRepolinks(): RepoLinks {
	const repos: RepoLinks = {
		src: '',
		dst: ''
	};
	const src = document.getElementById('sourceRepo');
	const dst = document.getElementById('targetRepo');
	if (!(src instanceof HTMLInputElement) || !(dst instanceof HTMLInputElement))
		return repos;
	if (!src || !dst)
		return repos;
	repos.src = src.value;
	repos.dst = dst.value;

	return repos;
}

function inform(content: string): void {
	const reply = document.getElementById('reply');
	if (!(reply instanceof HTMLDivElement))
		return;

	reply.textContent = content;
	reply.classList.remove('opacity-0', 'translate-y-4');
	reply.classList.add('opacity-100', 'translate-y-0');

	setTimeout(() => {
		reply.classList.remove('opacity-100');
		reply.classList.add('opacity-0');
	}, 5000);
}

export { RepoLinks };
export { getRepolinks, inform };
