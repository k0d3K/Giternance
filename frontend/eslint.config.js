import tseslint from "@typescript-eslint/eslint-plugin";	// Import linter
import tsparser from "@typescript-eslint/parser";			// Import parser
import tsimport from "eslint-plugin-import";				// Prevent issues with misspelling of file paths and import names
import stylistic from "@stylistic/eslint-plugin";			// Plugin for styling rules

export default [
	{
		files: ["./frontend/src/**/*.ts", "./shared/**/*.ts"],	// check all .ts files from src directory only, to not include futures config files in .ts format
		languageOptions: {
			parser: tsparser,
			parserOptions: {
				ecmaVersion: "latest",
				sourceType: "module",
				project: "./frontend/tsconfig.json",
			},
		},
		plugins: {
			"@typescript-eslint": tseslint,
			"import": tsimport,
			"@stylistic": stylistic,
		},
		rules: {
			// --- General format ---
			"@stylistic/indent": ["error", "tab", { "SwitchCase": 1 }], // Enforces tabs for indentation even for cases inside switchs
			"@stylistic/no-mixed-spaces-and-tabs": ["error"], // Forbids mixing spaces and tab

			// --- Naming conventions ---
			"@typescript-eslint/naming-convention": [ "error", {
				selector: ["class", "interface", "typeAlias", "enum", "typeParameter"],
				format: ["PascalCase"],
				leadingUnderscore: "forbid",
				trailingUnderscore: "forbid",
			},
			{
				selector: ["variable", "parameter", "function", "method", "property", "parameterProperty", "accessor"],
				format: ["camelCase"],
				leadingUnderscore: "forbid",
				trailingUnderscore: "forbid",
			},
			{
				selector: "property",
				modifiers: ["requiresQuotes"],
				format: null
			},
			{
				selector: ["objectLiteralProperty", "typeProperty"],
				format: null
			},
			{
				selector: "property",
				modifiers: ["static", "readonly"],
				format: ["UPPER_CASE"],
				leadingUnderscore: "forbid",
				trailingUnderscore: "forbid"
			},
			{
				selector: ["variable"],
				modifiers: ["global"],
				format: ["UPPER_CASE"],
				leadingUnderscore: "forbid",
				trailingUnderscore: "forbid",
			},
			{
				selector: "enumMember",
				format: ["UPPER_CASE"],
				leadingUnderscore: "forbid",
				trailingUnderscore: "forbid",
			}],

			// --- Class & instantiation rules ---
			"new-parens": "error",					// Enforce parentheses on all constructor calls
			"no-new-wrappers": "error",				// Enforce use of primitive literals
			"no-array-constructor": "error",

			// --- Variable declaration rules ---
			"no-var": "error",						// Always use `const` or `let` to declare variables
			"prefer-const": "error",				// Suggest using `const` where possible

			// --- Exception handling ---
			"no-throw-literal": "error",			// Enforce `throw new Error()` instead of throwing plain strings or numbers

			// --- Code style & braces ---
			"@stylistic/curly-newline": ["error"],	// Require braces for blocks (if, else, while, for, ...)
			"@stylistic/object-curly-spacing": ["error", "always"],	// Require a space before and after brackets
			"@stylistic/space-before-blocks": ["error", "always"],	// Require a space before blocks
			"@stylistic/nonblock-statement-body-position": ["error", "below"],	// There can be a single statement instead of a block on a new line
			"@stylistic/brace-style": ["error"],	// Enfore `one true brace style` (1tbs)
			"@stylistic/semi": ["error", "always"],	// Always require semicolons

			// --- Switch cases ---
			"default-case": ["error"],				// Must include a default case into switch cases
			"no-fallthrough": ["error", { "allowEmptyCase": true }],	// Prevents letting one case “fall through” to the next, except if he is empty

			// --- Equality ---
			"eqeqeq": ["error"],					// Forces use of === and !==

			// --- Function style ---
			"func-style": ["error", "declaration"], // Requires the use of function declarations instead of function expressions
			"prefer-arrow-callback": ["error", { "allowNamedFunctions": false }],	// Prefer arrow functions for callbacks
			"arrow-body-style": ["error", "as-needed"],	// Only use {} in arrow functions if necessary

			// --- TypeScript strictness ---
			"@typescript-eslint/consistent-type-assertions": [ "error", { "assertionStyle": "never" }],	// Forbids as Type assertions
			"@typescript-eslint/no-non-null-assertion": "error",	//	Forbids ! non-null assertions

			// --- Enums ---
			"no-restricted-syntax": ["error", {		// Forbis const enums
					selector: "TSEnumDeclaration[const=true]",
					message: "Avoid using const enums.",
				},
			],

			// --- Source Organization ---
			"@typescript-eslint/no-namespace": "error",	// Disallows namespace (use ES modules instead)
			"@typescript-eslint/no-require-imports": "error",	// Disallows require() imports (use import syntax)

			// --- Imports / Exports ---
			"import/no-default-export": "error",	// Forbis export default

			// --- Type system ---
			"@typescript-eslint/no-inferrable-types": "error",
			"@typescript-eslint/explicit-function-return-type": "error",	// Always require return type annotations for functions and methods
			"@typescript-eslint/no-explicit-any": "error",	// Forbids any → must use concrete or generic types
			"@typescript-eslint/consistent-type-definitions": ["error", "interface"],	// Always use interface instead of type for objects
			"@typescript-eslint/array-type": ["error", {	// Enforces simple array types → string[] instead of Array<string>
					default: "array-simple",
					readonly: "array-simple"
				}
			]
		}
	}
];
