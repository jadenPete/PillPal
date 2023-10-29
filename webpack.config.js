const path = require("path");

module.exports = {
	entry: {
		allMedication: "./pill_pal/static/ts/allMedication.tsx",
		itemviewer: "./pill_pal/static/ts/itemviewer.tsx"
	},

	externals: {
		"bootstrap": "bootstrap",
		"react": "React",
		"react-dom": "ReactDOM"
	},

	output: {
		filename: "[name].js",
		path: path.resolve(__dirname, "pill_pal", "static", "js"),
	},

	module: {
		rules: [
			{
				test: /\.tsx?$/,
				loader: "ts-loader"
			}
		]
	},

	resolve: {
		extensions: [".js", ".ts", ".tsx"]
	}
};
