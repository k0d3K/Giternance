import fastify from "fastify";
import fastifyStatic from "@fastify/static";

const APP = fastify();

// Serve static files
APP.register(fastifyStatic, {
	root: "/app/dist",
	prefix: "/dist/"
});

APP.register(fastifyStatic, {
	root: "/app/public",
	prefix: "/",
	decorateReply: false,
	index: ["index.html"]
});

// --- Start server ---
async function start(): Promise<void> {
	try {
		console.log(`Frontend running !`);
		await APP.listen({ port: 3030, host: "0.0.0.0" });
	} catch (err) {
		console.error(err);
		process.exit(1);
	}
};

start();
