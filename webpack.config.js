const path = require("path");

module.exports = {
	entry: {
    // for each page, append to dict in the format:
    // name: "./static/ts/{filename}.tsx",
    index: "./static/ts/index.tsx", 
    itemviewer: "./static/ts/itemviewer.tsx"
  },
	externals: {
		"bootstrap": "bootstrap",
		"react": "React",
		"react-dom": "ReactDOM"
	},

	output: {
	  filename: "[name].js",
	  path: path.resolve(__dirname, "static", "js"),
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
