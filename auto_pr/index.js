const core = require("@actions/core");
const { Octokit } = require("@octokit/core");

const octokit = new Octokit({
  auth: process.env.RUNEQL_DATA_PUSH,
});

octokit
  .request("POST /repos/{owner}/{repo}/pulls", {
    owner: "schmidlidev",
    repo: "runeql-data",
    head: "update",
    base: "main",
    title: "OSRSBOX Data Update",
  })
  .then((res) => {
    console.log(res);
  })
  .catch((err) => {
    console.log(err);
  });
